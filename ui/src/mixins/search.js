import { searchApi } from "@/api/api";
import { storeMixin } from "./store";

export const searchMixin = {
    data(){
        return {
            searchApi: searchApi,
        }
    }
}


const TOPS_LIMIT = import.meta.env.VITE_TOPS_LIMIT || 1

export const topsMixin = {
    mixins: [storeMixin],
    props: {
        topData: Array,
    },
    data(){
        return {
            type: 'port',
        }
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
            const query = this.$route.query
            this.store.setDetails(this.topData)
            this.$router.push(`/details?t=${query.t}&q=${query.q}&facet=${this.type}`)
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