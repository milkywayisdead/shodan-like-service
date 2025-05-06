import { searchApi } from "@/api/api";
import { storeMixin } from "./store";
import { DETAILS_MAX_ITEMS } from '@/utils/constants'


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
            facet: null,
            series: [],
            categories: [],
            _categories: []
        }
    },
    computed: {
        filterIsComplex(){
            const query = this.$route.query
            return !!query.et && !!query.eq
        },
        maxItemsExceeded(){
            return this._categories.length > DETAILS_MAX_ITEMS
        }
    },
    methods: {
        setDetails(data){
            const cats = []
            data.forEach(item => {
                if(item._id.includes(' ')){
                    cats.push(item._id.split(' '))
                } else {
                    cats.push(item._id)
                }
                this._categories.push(item._id)
            })
            this.categories = cats
            
            this.series = [
                data.reduce((acc, item) => {
                    acc.data.push(item.count)
                    return acc
                }, {name: 'details', data: []})
            ]
        },
        getDetails(){
            const query = this.$route.query
            const t = query.t
            const q = query.q
            const facet = query.facet
            const et = query.et
            const eq = query.eq

            this.store.setLoading()
            searchApi.details(t, q, facet, et, eq)
                .then(res => {
                    if(res.status === 200){
                        const k = Object.keys((res.data.details[0]))
                        this.setDetails(res.data.details[0][k[0]])
                    }
                }).catch(err => {}).finally(() => {
                    setTimeout(this.store.resetLoading, 500)
                })
        },
        extendedSearch(term){
            const q = this.$route.query
            if(q.t === 'net' && this.facet){
                this.$router.push(`/search?t=${q.t}&q=${q.q}&et=${this.facet}&eq=${term}`)
            }
        }
    },
    mounted(){
        this.getDetails()
    },
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
            const et = query.et
            const eq = query.eq

            let path = `/details?t=${query.t}&q=${query.q}&facet=${this.type}`
            if(!!et && !!eq){
                path = `${path}&et=${et}&eq=${eq}`
            }
            this.$router.push(path)
        },
    }
}


export const genericResultsMixin = {
    props: {
        info: {
            type: Object,
            default: {}
        },
        query: String,
    },
    emits: ['host-clicked'],
    methods: {
        emitHostClicked(host){
            this.$emit('host-clicked', host)
        },
        appendSearchParams(type, searchParams){
            searchParams.originalType = type
            searchParams.originalQuery = this.query
            return searchParams
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


export const searchFacetMixin = {
    emits: ['facet-clicked'],
    methods: {
        emitParamClickedOrIgnore(param, value, ignore=false){
            if(ignore) return
            this.$emit('facet-clicked', {param, value})
        }
    }
}


export const searchJumpMixin = {
    emits: ['search-by', 'extend-search'],
    methods: {
        emitSearchBy(newSearch){
            this.$emit('search-by', newSearch)
        },
        emitExtendSearch(newSearch){
            this.$emit('extend-search', newSearch)
        },
        extendedSearch(value){
            return {
                param: this.type,
                value: value,
            }
        }
    },
}