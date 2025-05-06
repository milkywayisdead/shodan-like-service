<template>
<h3>{{ locale.search.details }}</h3>
<bar-chart v-if="categories.length"
    :categories="categories"
    :_categories="_categories"
    :series="series" 
    @category-click="extendedSearch" />
</template>

<script>
import { detailsMixin } from '@/mixins/search'

export default {
    data(){
        return {
            facet: 'app'
        }
    },
    mixins: [detailsMixin],
}
</script>