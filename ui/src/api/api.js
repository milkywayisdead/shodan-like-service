import axios from "axios";
import { getCSRFToken } from "@/stores/auth";
import router from "@/router";
import { useAuthStore } from "@/stores/auth";
import { useAppStore } from "@/stores/app";

const auth = useAuthStore()
const store = useAppStore()

const api = axios.create({
    baseURL: import.meta.env.VITE_SEARCH_URL,
})

api.interceptors.request.use(
    config => {
        config.headers['X-CSRFToken'] = getCSRFToken()
        config.withCredentials = true
        return config;
    },
    error => {
        return Promise.reject(error)
    }
)

api.interceptors.response.use(
    response => {
        return response
    }, 
    error => {
        if(error.status === 401){
            auth.user = null
            auth.isAuthenticated = false
            auth.saveState()
            router.replace('/login')
        }
        return Promise.reject(error)
    }
)


export const searchApi = {
    hosts(params){
        return api.get('/hosts', params)
    },
    port(params){
        return api.get('/port', params)
    },
    net(params){
        return api.get('/net', params)
    },
    asn(params){
        return api.get('/asn', params)
    },
    domain(params){
        return api.get('/domain', params)
    },
    country(params){
        return api.get('/country', params)
    },
    city(params){
        return api.get('/city', params)
    },
    org(params){
        return api.get('/org', params)
    },
    app(params){
        return api.get('/app', params)
    },
    component(params){
        return api.get('/component', params)
    },
    soft(params){
        return api.get('/soft', params)
    },
    os(params){
        return api.get('/os', params)
    },
    service(params){
        return api.get('/service', params)
    },
    pagination: {
        net(params){
            return api.get('/net/page', params)
        },
        port(params){
            return api.get('/port/page', params)
        },
        asn(params){
            return api.get('/asn/page', params)
        },
        app(params){
            return api.get('/app/page', params)
        },
        component(params){
            return api.get('/component/page', params)
        },
        org(params){
            return api.get('/org/page', params)
        },
        country(params){
            return api.get('/country/page', params)
        },
        city(params){
            return api.get('/city/page', params)
        },
        soft(params){
            return api.get('/soft/page', params)
        },
        service(params){
            return api.get('/service/page', params)
        },
        os(params){
            return api.get('/os/page', params)
        },
    },
    details(t, q, facet){
        const params = {params: {t, q, facet}}
        return api.get('/details', params)
    }
}