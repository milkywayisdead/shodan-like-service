<template>
<search-bar ref="searchBar" @search="searchTheSame" />
<component v-if="searchType && !noResults"
    :is="`${searchType}-search-results`" 
    :info="results"
    @host-clicked="hostClickedHandler($event)" 
    @search-by="handleSearchBy" 
    @extend-search="extendSearch" 
    :query="query" />
<no-results v-if="noResults" />
<v-pagination v-if="auth.isAuthenticated && paginationLength"
    v-model="page" 
    :length="paginationLength" 
    :total-visible="totalVisible" />
</template>

<script>
import { storeMixin } from '@/mixins/store';
import { searchMixin } from '@/mixins/search';
import { authMixin } from '@/mixins/auth';

import HostsSearchResults from '@/components/search/results/HostsSearchResults.vue';
import NetSearchResults from '@/components/search/results/NetSearchResults.vue';
import PortSearchResults from '@/components/search/results/PortSearchResults.vue';
import AsnSearchResults from '@/components/search/results/AsnSearchResults.vue';
import LocSearchResults from '@/components/search/results/LocSearchResults.vue';
import OrgSearchResults from '@/components/search/results/OrgSearchResults.vue';
import SoftSearchResults from '@/components/search/results/SoftSearchResults.vue';
import AppSearchResults from '@/components/search/results/AppSearchResults.vue';
import ComponentSearchResults from '@/components/search/results/ComponentSearchResults.vue';
import OsSearchResults from '@/components/search/results/OsSearchResults.vue';
import ServiceSearchResults from '@/components/search/results/ServiceSearchResults.vue';
import DomainSearchResults from '@/components/search/results/DomainSearchResults.vue';


export default {
    mixins: [storeMixin, searchMixin, authMixin],
    data(){
        return {
            results: {},
            page: 1,
            totalVisible: 5,
            pageLength: 10,
            paginationLimit: 20,
            _lockPage: false,
            searchType: 'hosts',
            query: '',
        }
    },
    computed: {
        paginationLength(){
            const hostsNum = this.results.hosts_total || 0
            const pagesNum = Math.ceil(hostsNum / this.pageLength)
            return pagesNum > this.paginationLimit ? this.paginationLimit : pagesNum
        },
        noResults(){
            if(this.searchType === 'hosts'){
                return this.results.host === null
            }
            return this.results.hosts_total === 0
        }
    },
    methods: {
        searchTheSame(params){
            this.search(params.t, params.q)
        },
        search(type, term, extraType, extraQuery){
            if(!term || !type) return
            const func = this.searchApi[type]
            this.store.setLoading()
            this.query = term

            let params = {search: term}
            if(!!extraType && !!extraQuery){
                params = {search: term, et: extraType, eq: extraQuery}
            }

            func({params: params})
                .then(res => {
                    this.searchType = type
                    const status = res.status
                    if(status === 200){
                        this.results = res.data
                        this.lockPage()
                        this.resetPage()
                        this.unlockPage()
                    }
                }).catch(err => {
                    if(err.status === 429){
                        this.store.addErrorNotif(this.locale.messages.requestsLimitReached)
                    }
                }).finally(() => {
                    setTimeout(() => {
                        this.store.resetLoading()
                    }, 500);
                })
        },
        getPage(page){
            page = page > 20 ? 20 : page
            const query = this.$route.query
            const term = query.q
            const func = this.searchApi.pagination[query.t]
            this.store.setLoading()
            func({params: {search: term, page: page}})
                .then(res => {
                    this.results.hosts = res.data.hosts
                }).catch(err => {}).finally(() => {
                    setTimeout(() => {
                        this.store.resetLoading()
                    }, 500);
                })
        },
        resetPage(){
            this.lockPage()
            this.page = 1
        },
        lockPage(){
            this._lockPage = true
        },
        unlockPage(){
            this._lockPage = false
        },
        hostClickedHandler(host){
            this.$router.push(`/search?t=hosts&q=${host.IP}`)
        },
        handleSearchBy(event){
            this.$router.push(`/search?t=${event.param}&q=${event.value}`)
        },
        extendSearch(params){
            this.$router.push(`/search?t=${params.originalType}&q=${params.originalQuery}&et=${params.param}&eq=${params.value}`)
        }
    },
    watch: {
        page(value){
            if(!this._lockPage){
                this.getPage(value)
            }
        },
        $route(to, from){
            const type = to.query.t || ''
            const term = to.query.q || ''
            const extraType = to.query.et || ''
            const extraQuery = to.query.eq || ''
            this.$refs.searchBar.setTypeAndTerm(type, term)
            this.search(type, term, extraType, extraQuery)
        }
    },
    mounted(){
        const query = this.$route.query || {}
        const type = query.t || ''
        const term = query.q || ''
        const extraType = query.et || ''
        const extraQuery = query.eq || ''
        this.$refs.searchBar.setTypeAndTerm(type, term)
        this.search(type, term, extraType, extraQuery)
    },
    components: {
        HostsSearchResults,
        NetSearchResults,
        PortSearchResults,
        AsnSearchResults,
        LocSearchResults,
        OrgSearchResults,
        SoftSearchResults,
        AppSearchResults,
        ComponentSearchResults,
        OsSearchResults,
        ServiceSearchResults,
        DomainSearchResults,
    },
}
</script>

<route lang="yaml">
meta:
    layout: search
</route>