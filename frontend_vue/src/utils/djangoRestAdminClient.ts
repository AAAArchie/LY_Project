import axios, {AxiosError, AxiosInstance, AxiosRequestConfig, AxiosResponse} from "axios";
import {computed, markRaw, ref, Ref, watchEffect} from "vue";
import DjangoRestAdminAuthenticator from "./djangoRestAdminAuthenticator";

interface List<Src> {
    count: number,
    next: string | null,
    previous: string | null,
    results: Src[],
}

export interface DjangoRestAdminOptions<Src extends object, Dst extends object = Src> {
    endpoint?: string,
    auth?: DjangoRestAdminAuthenticator
    placeholder?: Src // 在服务器有响应之前返回该值，这个是后处理之前的值
    listPlaceholderCount?: number // 列表项的默认数量
    axiosConfig?: AxiosRequestConfig // 使用这个配置从服务器获取数据
    manualActions?: string[] // 对这些 actions 不调用 onerror 和 parse 函数
    then?: (r: AxiosResponse, action: string) => Src // 服务器正常请求后，使用该函数进行处理，默认返回 r.data
    error?: (e: AxiosError, action: string) => Src // 服务器报错后，使用该函数进行处理，默认返回占位符
    parse?: (item: Src, action: string) => Dst // 不管是否报错，都使用该函数进行后处理
}

interface ParsedOptions<Src extends object, Dst extends object = Src> {
    endpoint: string,
    auth?: DjangoRestAdminAuthenticator
    placeholder: Src // 在服务器有响应之前返回该值
    axiosConfig: AxiosRequestConfig // 使用这个配置从服务器获取数据

    manualActions: string[] // 对这些 actions 不调用 onerror 和 parse 函数
    parse: (item: Src, action: string) => Dst // 不管是否报错，都使用该函数进行后处理

    then: (r: AxiosResponse, action: string) => Src
    error: (e: AxiosError, action: string) => Src
    parsedPlaceholder: Dst

    listParse: (i: List<Src>) => List<Dst>
    listError: (e: AxiosError) => List<Src>
    listPlaceholderCount?: number // 列表项的默认数量
    parsedListPlaceholder: List<Dst>
}

type PrimaryKey = string | number


/**
 * 对 REST 进行封装，提供详细的类型提示功能。
 *
 * 以下是一个示例。
 *
 * interface Base {
 *     id: number,
 *     name: string,
 *     count: number,
 * }
 *
 * export interface Src extends Base {
 * }
 *
 * export interface Dst extends Base {
 *     route: RouteLocationRaw,
 * }
 *
 * export const placeholder: Src = {
 *     count: 0,
 *     id: -1,
 *     name: "加载中",
 * }
 * export const parse = (src: Src): Dst => ({
 *     ...src, route: {name: RouteName.blogCategory.toString(), params: {categoryName: src.name}}
 * })
 *
 * export const client = new DjangoRestAdminClient<BlogCategory.Src, BlogCategory.Dst>({
 *     endpoint: `${Clients.baseEndpoint}/v2/blog/category/`,
 *     placeholder: BlogCategory.placeholder,
 *     auth: this.auth,
 *     parse: BlogCategory.parse,
 * })
 *
 */
export class DjangoRestAdminClient<GlobalSrc extends object, GlobalDst extends object> {
    private _client: AxiosInstance
    private readonly _options: DjangoRestAdminOptions<GlobalSrc, GlobalDst>

    constructor(options: DjangoRestAdminOptions<GlobalSrc, GlobalDst>) {
        this._options = options

        // 当token更新时刷新client
        const clientConfig = computed(() => ((this._options.auth?.vueMonitor() || true) && {
            baseURL: this._options.endpoint,
            headers: this._options.auth?.token?.value ? {'Authorization': `JWT ${this._options.auth.token.value}`} : {}
        }))
        this._client = axios.create(clientConfig.value)
        watchEffect(() => this._client = axios.create(clientConfig.value))
    }

    /**
     * 将方法独立传入的参数与全局参数进行合并。
     * 例如，可以在全局指定 auth 而在局部指定 onerror 处理方法。
     * 这样可以实现高度解耦。
     * @param action 根据调用的方法判断是否移除 parse 和 onerror 方法
     * @param options 各个方法传入的参数
     * @private
     */
    private _combineOptions<Src extends object = GlobalSrc, Dst extends object = GlobalDst>(action: string, options?: DjangoRestAdminOptions<Src, Dst>): ParsedOptions<Src, Dst> {
        const globalOptions = {...this._options}
        const manualActions = globalOptions.manualActions || []
        if (manualActions.includes(action)) {
            globalOptions.then = () => {
                throw `The action "${action}" has no "then" callback.`
            }
            globalOptions.error = () => {
                throw `The action "${action}" has no "error" callback.`
            }
            globalOptions.parse = () => {
                throw `The action "${action}" has no "parse" callback.`
            }
        }
        const axiosConfig = {...globalOptions.axiosConfig, ...options?.axiosConfig}
        options = {...globalOptions, ...options, axiosConfig} as DjangoRestAdminOptions<Src, Dst>
        return this._parseOption(options)
    }

    /**
     * 对用户传入的参数组进行预处理。
     * 用户可能传入一部分参数，例如可能传入了 placeholder 但没有传入 onerror 。
     * 本方法可以实现类似于将 onerror 设置为自动设置为 placeholder 的功能等。
     * @param options
     * @private
     */
    private _parseOption<Src extends object = GlobalSrc, Dst extends object = GlobalDst>(options: DjangoRestAdminOptions<Src, Dst>): ParsedOptions<Src, Dst> {
        const endpoint = options.endpoint || '/'
        const placeholder = options.placeholder || {} as Src
        const manualActions = options.manualActions || []

        const then = (r: AxiosResponse, action: string) => {
            if (!options.then) return r.data
            return options.then(r, action)
        }

        const error = (error: AxiosError, action: string) => {
            if (!options.error) return placeholder
            return options.error(error, action)
        }

        const parse = (src: Src, action: string) => {
            if (!options.parse) return <Dst><unknown>src
            try {
                return options.parse(src, action)
            } catch (e) {
                console.error(`Parser of "${endpoint}" has error, src="${JSON.stringify(src)}"`)
                throw e
            }
        }
        const listPlaceholderCount = options.listPlaceholderCount || 3
        const listPlaceholder: List<Src> = {
            count: listPlaceholderCount, next: null, previous: null,
            results: [...Array(listPlaceholderCount).keys()].map(_ => placeholder)
        }
        const listError = () => listPlaceholder
        const listParse = (src: List<Src>) => ({
            ...src,
            results: src.results.map(i => parse(i, 'list'))
        } as List<Dst>)
        const parsedPlaceholder = parse(options.placeholder || {} as Src, 'retrieve')
        const parsedListPlaceholder = listParse(listPlaceholder)
        const axiosConfig = options.axiosConfig || {}
        return {
            endpoint, listPlaceholderCount, parsedPlaceholder, parsedListPlaceholder,
            placeholder, axiosConfig, manualActions,
            then, error, parse, listParse, listError,
            ...options
        }
    }


    public async list<Src extends object = GlobalSrc, Dst extends object = GlobalDst>(options?: DjangoRestAdminOptions<Src, Dst>): Promise<List<Dst>> {
        const op = this._combineOptions('list', options)
         console.log(op)
        return await this._client.get(op.endpoint, op?.axiosConfig).then(i => i.data)
            .catch(e => op.listError(e)).then(op.listParse)
    }

    public async retrieve<Src extends object = GlobalSrc, Dst extends object = GlobalDst>(pk: PrimaryKey, options?: DjangoRestAdminOptions<Src, Dst>): Promise<Dst> {
        const action = 'retrieve'
        const op: ParsedOptions<Src, Dst> = this._combineOptions(action, options)
        return await this._client.get(`${op.endpoint}${pk}/`, op.axiosConfig).then(i => op.then(i, action)).catch(e => op.error(e, action)).then(i => op.parse(i, action))
    }

    public async put<Src extends object = GlobalSrc, Dst extends object = GlobalDst>(id: PrimaryKey, data: Src, options?: DjangoRestAdminOptions<Src, Dst>): Promise<Dst> {
        const action = 'put'
        const op = this._combineOptions(action, options)
        return await this._client.put(`${op.endpoint}${id}/`, data, options?.axiosConfig).then(i => op.then(i, action)).catch(e => op.error(e, action)).then(i => op.parse(i, action))
    }

    public async patch<Src extends object = GlobalSrc, Dst extends object = GlobalDst>(id: string | number, data: Src, options?: DjangoRestAdminOptions<Src, Dst>): Promise<Dst> {
        const action = 'patch'
        const op = this._combineOptions(action, options)
        return await this._client.patch(`${op.endpoint}${id}/`, data, op.axiosConfig).then(i => op.then(i, action)).catch(e => op.error(e, action)).then(i => op.parse(i, action))
    }

    public async action<Src extends object = GlobalSrc, Dst extends object = GlobalDst>(actionName: string, pk?: PrimaryKey, options?: DjangoRestAdminOptions<Src, Dst>): Promise<Dst> {
        const action = actionName
        const op = this._combineOptions(action, options)
        const url = `${op.endpoint}${(pk + "/") || ""}${actionName}/`
        const config = {method: 'get', url, ...op.axiosConfig} as AxiosRequestConfig
        return this._client.request(config).then(i => op.then(i, action)).catch(e => op.error(e, action)).then(i => op.parse(i, action))
    }

    public async post<Src extends object = GlobalSrc, Dst extends object = GlobalDst>(data: Src, options?: DjangoRestAdminOptions<Src, Dst>): Promise<Dst> {
        const action = 'post'
        const op = this._combineOptions(action, options)
        return await this._client.post(op.endpoint, data, op.axiosConfig).then(i => op.then(i, action)).catch(e => op.error(e, action)).then(i => op.parse(i, action))
    }

    public async delete<Src extends object = GlobalSrc, Dst extends object = GlobalDst>(pk: PrimaryKey, data: Src, options?: DjangoRestAdminOptions<Src, Dst>): Promise<boolean> {
        const op = this._combineOptions('delete', options)
        return await this._client.delete(`${op.endpoint}${pk}/`, op.axiosConfig).then(() => true).catch(() => false)
    }


    /**
     * 当参数发生变化之后，重新进行获取
     * @param options
     */
    public refList<Src extends object = GlobalSrc, Dst extends object = GlobalDst>(options?: Ref<DjangoRestAdminOptions<Src, Dst>>): Ref<List<Dst>> {
        const op = computed(() => this._combineOptions('list', options?.value))
        const response = ref(markRaw(op.value.parsedListPlaceholder)) as Ref<List<Dst>>
        watchEffect(async () => response.value = markRaw(await this.list(options?.value)))
        return response
    }

    public refRetrieve<Src extends object = GlobalSrc, Dst extends object = GlobalDst>(pk: Ref<PrimaryKey>, options?: Ref<DjangoRestAdminOptions<Src, Dst>>): Ref<Dst> {
        const op = computed(() => this._combineOptions('retrieve', options?.value))
        const response = ref(markRaw(op.value.parsedPlaceholder)) as Ref<Dst>
        watchEffect(async () => response.value = markRaw(await this.retrieve(pk.value, options?.value)))
        return response
    }

    public refAction<Src extends object = GlobalSrc, Dst extends object = GlobalDst>(actionName: Ref<string>, pk?: Ref<PrimaryKey>, options?: Ref<DjangoRestAdminOptions<Src, Dst>>): Ref<Dst> {
        const op = computed(() => this._combineOptions(actionName.value, options?.value))
        const response = ref(markRaw(op.value.parsedPlaceholder)) as Ref<Dst>
        watchEffect(async () => response.value = markRaw(await this.action(actionName.value, pk?.value, options?.value)))
        return response
    }
}
