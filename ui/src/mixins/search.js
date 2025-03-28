import { searchApi } from "@/api/api";

export const searchMixin = {
    data(){
        return {
            searchApi: searchApi,
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