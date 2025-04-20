import { searchApi } from "@/api/api";
import { storeMixin } from "./store";

export const searchMixin = {
    data(){
        return {
            searchApi: searchApi,
        }
    }
}


export const detailsMixin = {
    mixins: [storeMixin],
    data(){
        return {
            _chartData: {
                labels: [],
                datasets: []
            },
        }
    },
    methods: {
        setDetails(data){
            const labels = data.map(item => item._id)
            const datasets = [
                {
                    data: data.map(item => item.count),
                    backgroundColor: '#36a2eb',
                }
            ]
            this._chartData = {
                labels: labels,
                datasets: datasets,
            }
        },
        getDetails(){
            const query = this.$route.query
            const t = query.t
            const q = query.q
            const facet = query.facet
            this.store.setLoading()
            searchApi.details(t, q, facet)
                .then(res => {
                    if(res.status === 200){
                        const k = Object.keys((res.data.details[0]))
                        this.setDetails(res.data.details[0][k[0]])
                    }
                }).catch(err => {}).finally(() => {
                    setTimeout(this.store.resetLoading, 500)
                })
        }
    },
    mounted(){
        this.getDetails()
    },
    computed: {
        chartData(){
            return this._chartData
        }
    }
}


const TOPS_LIMIT = import.meta.env.VITE_TOPS_LIMIT || 5

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
        filteredItems(){
            return (this.topData || []).filter(item => {
                return item._id !== ''
            })
        },
        items(){
            return this.filteredItems.slice(0, TOPS_LIMIT)
        },
        showMore(){
            return (this.topData || []).length > TOPS_LIMIT
        },
    },
    methods: {
        toMore(){
            const query = this.$route.query
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