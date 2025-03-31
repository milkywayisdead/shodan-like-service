<template>
<search-bar ref="searchBar" />
<component v-if="type"
    ref="details"
    :is="`${this.type}-details`" />
</template>

<script>
import PortDetails from '@/components/search/details/PortDetails.vue';
import ApplicationDetails from '@/components/search/details/ApplicationDetails.vue';
import SoftwareDetails from '@/components/search/details/SoftwareDetails.vue';
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
    },
    components: {
        PortDetails,
        ComponentDetails,
        SoftwareDetails,
        ServiceDetails,
        ApplicationDetails,
    }
}
</script>

<route lang="yaml">
meta:
    layout: search
</route>