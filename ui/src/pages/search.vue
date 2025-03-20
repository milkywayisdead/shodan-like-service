<template>
<h1>ДОБАВИТЬ ПРОВЕРКУ НА АВТОРИЗАЦИЮ</h1>
<search-bar ref="searchBar" @search="search" />
<component :is="`${searchType}-search-results`" v-if="searchType" />
</template>

<script>
import { storeMixin } from '@/mixins/store';
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
import { searchMixin } from '@/mixins/search';

export default {
    mixins: [storeMixin, searchMixin],
    computed: {
        searchType(){
            return this.store.searchType
        },
    },
    methods: {
        search(params){
            const term = params.term
            if(!term) return
            const func = this.searchApi[params.type]
            func({params: {search: term}})
                .then(res => {
                    if(res.status === 200){
                        console.log(res.data)
                        this.store.setSearchType(params.type)
                    }
                }).catch(err => {})
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