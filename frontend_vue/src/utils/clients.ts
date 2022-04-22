import DjangoRestAdminAuthenticator from "./djangoRestAdminAuthenticator";
import {DjangoRestAdminClient} from "./djangoRestAdminClient";
import constants from "../utils/constants";

namespace MergedImages {
    interface IdentificationDetailSrc {
        id?: 107
        user?: string
        upload_images?: string
        nation1?: string
        nation2?: string
        nation3?: string
        modified_nation?: null
        time_consuming?: string
    }

    interface IdentificationDetailDst {
        id: number
        user: string
        upload_images: string
        nation1: string
        nation2: string
        nation3: string
        modified_nation: string | null
        time_consuming: string
    }

    export interface Src {
        id?: number
        user?: string
        detail_url?: string
        background_name?: string
        result_image?: string
        person_1_head_image?: string
        person_2_head_image?: string
        person_1_identification?: number
        person_2_identification?: number
        person_1_identification_detail?: IdentificationDetailSrc
        person_2_identification_detail?: IdentificationDetailSrc
    }

    export interface Dst {
        id: number
        user: string
        detail_url: string
        background_name: string
        background_image_url: string
        result_image: string
        person_1_head_image: string
        person_2_head_image: string
        person_1_identification: number
        person_2_identification: number
        person_1_identification_detail: IdentificationDetailDst
        person_2_identification_detail: IdentificationDetailDst
    }

    export const placeholder: Src = {
        id: -1,
        user: 'Anonymous',
        detail_url: '',
        background_name: 'bg1',
        result_image: '',
        person_1_head_image: '',
        person_2_head_image: '',
        person_1_identification: -1,
        person_2_identification: -1,
        person_1_identification_detail: {},
        person_2_identification_detail: {},
    }
    const parseDetail = (src: IdentificationDetailSrc): IdentificationDetailDst => {
        return {
            id: src.id || -1,
            user: src.user || '',
            upload_images: src.upload_images || '',
            nation1: src.nation1 || '',
            nation2: src.nation2 || '',
            nation3: src.nation3 || '',
            modified_nation: src.modified_nation || '',
            time_consuming: src.time_consuming || '',
        }
    }
    export const parse = (src: Src): Dst => {

        const result: Dst = Object.assign({}, <unknown>src, {
            id: src.id || -1,
            user: src.user || 'Anonymous',
            detail_url: src.detail_url || '',
            background_name: src.background_name || '',
            result_image: src.result_image || '',
            person_1_head_image: src.person_1_head_image || '',
            person_2_head_image: src.person_2_head_image || '',
            person_1_identification: src.person_1_identification || -1,
            person_2_identification: src.person_2_identification || -1,
            person_1_identification_detail: parseDetail(src.person_1_identification_detail || {}),
            person_2_identification_detail: parseDetail(src.person_2_identification_detail || {}),
        }) as Dst
        result.background_image_url = `${constants.apiUrl}/media/background-image/${result.background_name}.png`
        return result
    }
}

class Clients {
    public auth = new DjangoRestAdminAuthenticator(`${constants.host}api/token/`)
    public v图片合成过程 = new DjangoRestAdminClient<MergedImages.Src, MergedImages.Dst>({ // 泛型
        endpoint: `${constants.apiUrl}merged-images/`,
        placeholder: MergedImages.placeholder,
        auth: this.auth, parse: MergedImages.parse,
    })
}

const clients = new Clients()
export default clients