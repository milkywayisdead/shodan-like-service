<template>
<search-bar ref="searchBar" host-details />
<component v-if="type"
    ref="details"
    :is="`${this.type}-details`" />
</template>

<script>
import PortDetails from '@/components/search/details/PortDetails.vue';
import AppDetails from '@/components/search/details/AppDetails.vue';
import SoftDetails from '@/components/search/details/SoftDetails.vue';
import ServiceDetails from '@/components/search/details/ServiceDetails.vue';
import ComponentDetails from '@/components/search/details/ComponentDetails.vue';

export default {
    data(){
        return {
            type: '',
        }
    },
    methods: {
        getQuery(){
            return this.$route.query || {t: '', q: ''}
        }
    },
    mounted(){
        const query = this.getQuery()
        this.type = query.facet
        this.$refs.searchBar.setTypeAndTerm(query.t, query.q)
        this.$nextTick(() => {
            this.$refs.details.setDetails()
        })
    },
    components: {
        PortDetails,
        ComponentDetails,
        SoftDetails,
        ServiceDetails,
        AppDetails,
    }
}
</script>

<route lang="yaml">
meta:
    layout: search
</route>