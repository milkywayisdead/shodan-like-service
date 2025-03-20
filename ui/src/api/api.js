import axios from "axios";

const api = axios.create()
const searchApiUrl = import.meta.env.VITE_SEARCH_URL

export const searchApi = {
    hosts(params){
        return api.get(`${searchApiUrl}/hosts`, params)
    },
    port(params){
        return api.get(`${searchApiUrl}/port`, params)
    },
    net(params){
        return api.get(`${searchApiUrl}/net`, params)
    },
    asn(params){
        return api.get(`${searchApiUrl}/asn`, params)
    },
    domain(params){
        return api.get(`${searchApiUrl}/domain`, params)
    },
    loc(params){
        return api.get(`${searchApiUrl}/loc`, params)
    },
    org(params){
        return api.get(`${searchApiUrl}/org`, params)
    },
    app(params){
        return api.get(`${searchApiUrl}/app`, params)
    },
    component(params){
        return api.get(`${searchApiUrl}/component`, params)
    },
    soft(params){
        return api.get(`${searchApiUrl}/soft`, params)
    },
    os(params){
        return api.get(`${searchApiUrl}/os`, params)
    },
    service(params){
        return api.get(`${searchApiUrl}/service`, params)
    },
}