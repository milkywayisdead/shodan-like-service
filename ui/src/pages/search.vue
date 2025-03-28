<template>
<search-bar ref="searchBar" @search="search" />
<component v-if="searchType"
    :is="`${searchType}-search-results`" 
    :info="results"
    @host-clicked="hostClickedHandler($event)" />
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
        }
    },
    computed: {
        searchType(){
            return this.store.searchType
        },
        paginationLength(){
            const hostsNum = this.results.hosts_total || 0
            const pagesNum = Math.ceil(hostsNum / this.pageLength)
            return pagesNum > this.paginationLimit ? this.paginationLimit : pagesNum
        }
    },
    methods: {
        search(params){
            const term = params.term
            if(!term) return
            const func = this.searchApi[params.type]
            this.store.setLoading()
            this.store.setSearchType(params.type)
            func({params: {search: term}})
                .then(res => {
                    const status = res.status
                    if(status === 200){
                        this.results = res.data
                        this.lockPage()
                        this.resetPage()
                        this.unlockPage()
                    }
                }).catch(err => {}).finally(() => {
                    setTimeout(() => {
                        this.store.resetLoading()
                    }, 500);
                })
        },
        getPage(page){
            const term = this.store.searchTerm
            page = page > 20 ? 20 : page
            const func = this.searchApi.pagination[this.store.searchType]
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
            this.store.setHostDetails(host)
            this.$router.push('/details/host')
        }
    },
    watch: {
        page(value){
            if(!this._lockPage){
                this.getPage(value)
            }
        }
    },
    mounted(){
        this.$refs.searchBar.searchType = this.store.searchType
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