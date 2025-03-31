import { searchApi } from "@/api/api";

export const searchMixin = {
    data(){
        return {
            searchApi: searchApi,
        }
    }
}


export const routeWatcher = {
    
}


const TOPS_LIMIT = import.meta.env.VITE_TOPS_LIMIT || 1

export const topsMixin = {
    props: {
        topData: Array,
    },
    computed: {
        items(){
            return (this.topData || []).slice(0, TOPS_LIMIT)
        },
        showMore(){
            return (this.topData || []).length > TOPS_LIMIT
        },
    },
    methods: {
        toMore(){
           
        },
    }
}


export const genericResultsMixin = {
    props: {
        info: {
            type: Object,
            default: {}
        }
    },
    emits: ['host-clicked'],
    methods: {
        emitHostClicked(host){
            this.$emit('host-clicked', host)
        }
    },
    computed: {
        totals(){
            const ports = (this.info.ports || [])[0]
            return {
                hosts: this.info.hosts_total,
                ports: ports?.total_ports_count || 0
            }
        }
    }
}