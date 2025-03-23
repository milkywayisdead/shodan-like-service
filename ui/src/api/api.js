import axios from "axios";
import { getCSRFToken } from "@/stores/auth";
import router from "@/router";
import { useAuthStore } from "@/stores/auth";

const auth = useAuthStore()

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
    loc(params){
        return api.get('/loc', params)
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
        loc(params){
            return api.get('/loc/page', params)
        },
    }
}