<template>
<search-bar ref="searchBar" host-details />
<component v-if="type"
    ref="details"
    :is="`${this.type}-details`" />
</template>

<script>
import HostsDetails from '@/components/search/details/HostsDetails.vue';
import PortDetails from '@/components/search/details/PortDetails.vue';

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
        this.type = query.facet || query.t
        this.$refs.searchBar.setTypeAndTerm(query.t, query.q)
        this.$nextTick(() => {
            this.$refs.details.setDetails()
        })
    },
    components: {
        HostsDetails,
        PortDetails,
    }
}
</script>

<route lang="yaml">
meta:
    layout: search
</route>