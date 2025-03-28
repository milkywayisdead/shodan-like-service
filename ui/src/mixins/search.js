import { searchApi } from "@/api/api";

export const searchMixin = {
    data(){
        return {
            searchApi: searchApi,
        }
    }
}


const TOPS_LIMIT = 1

export const topsMixin = {
    props: {
        topData: Array,
    },
    computed: {
        items(){
            return (this.topData || []).slice(0, TOPS_LIMIT)
        }
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