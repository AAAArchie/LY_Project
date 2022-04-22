import axios from "axios";
import {Ref, ref} from "vue";
import {fromUnixTime} from "date-fns";

interface JwtObtainResponseType {
    token: string,
    id: number,
    username: string,
    fullName: string,
}


interface TokenDetailResponseType {
    //从服务器直接获取到的token进行解析后的结果
    exp: number
    iat: number
    jti: string
    token_type: "access"
    user_id: number
}

class Token {
    private readonly _source: string;
    private readonly _sourceObject: JwtObtainResponseType; // 服务器响应原始数据
    public readonly value: string; // 实际的 token 值
    private readonly _tokenDetail: TokenDetailResponseType; // 从 token 中解析出来的数据
    public readonly issuedTime: Date; // 签发时间
    public readonly expiredTime: Date; // 过期时间
    public readonly userId: number; // 用户编号
    public fullName: string; // 可以用于显示的用户全名
    public userName: string // 用户的登录名

    constructor(source: string) {
        this._source = source;
        this._sourceObject = JSON.parse(this._source)
        this.value = this._sourceObject.token
        this._tokenDetail = JSON.parse(atob(this.value.split('.')[1])) as TokenDetailResponseType
        this.expiredTime = fromUnixTime(this._tokenDetail.exp)
        this.issuedTime = fromUnixTime(this._tokenDetail.iat)
        this.userId = this._tokenDetail.user_id
        this.fullName = this._sourceObject.fullName
        this.userName = this._sourceObject.username
    }

    toString = () => this.value

    get isExpired() { // 是否已过期
        return this.expiredTime < new Date()
    }
}

/**
 * 自动管理 Django Rest Framework JWT 的 Token。
 */
export default class DjangoRestAdminAuthenticator {
    private readonly _endpointUrl: URL
    private readonly _obtainUrl: URL
    private readonly _localStorageKey: string

    public _refStateMonitor: Ref<number>

    /**
     * 设置基本参数。
     * @param endpoint 类似 https://api.panhaoyu.com/jwt/，JWT服务器的根路径，应当以 / 结尾。
     * @param obtainUrl 类似 obtain/ 这样的不含域名的路径，不以 / 开头。
     * @param localStorageJwtKey 存储到 localStorage 中的键。
     */
    constructor(endpoint: string, obtainUrl: string = 'obtain/', localStorageJwtKey: string = 'jwt') {
        this._endpointUrl = new URL(endpoint)
        this._obtainUrl = new URL(obtainUrl, this._endpointUrl)
        this._localStorageKey = localStorageJwtKey;
        this._refStateMonitor = ref(1)

        //从缓存中读取之前存储的令牌
        let cachedToken = localStorage.getItem(this._localStorageKey) || ''
        cachedToken === '' || this._setToken(cachedToken)
    }

    // 处理令牌的多点存取过程
    private _token: Token | undefined;

    private _setToken(value: string): true {
        localStorage.setItem(this._localStorageKey, value)
        this._token = new Token(value)
        this._refStateMonitor.value += 1
        return true
    }

    private _delToken(): true {
        localStorage.removeItem(this._localStorageKey)
        this._token = undefined
        this._refStateMonitor.value += 1
        return true
    }

    //登录与登出
    public login = async (username: string, password: string): Promise<boolean> => await
        axios.post(this._obtainUrl.toString(), {username, password})
            .then(r => r.data).catch(_ => undefined)
            .then(data => data === undefined ? this._delToken() : this._setToken(JSON.stringify(data)))
            .then(_ => this.isLoggedIn)
    public logout = async (): Promise<boolean> => this._delToken() && true

    get token(): Token | undefined {
        if (this._token === undefined) return undefined // 如果不存在，直接返回不存在
        if (!this._token.isExpired) return this._token // 如果存在且没过期，则返回这个令牌
        return this._delToken() && undefined // 如果信息存在但是过期了，则删除这个令牌
    }

    get isLoggedIn(): boolean { // 当前登录状态
        return this.token !== undefined && !this.token.isExpired
    }

    vueMonitor = (): true => this._refStateMonitor.value > 0 && true || true // 与 Vue 进行集成，触发监控信号
}