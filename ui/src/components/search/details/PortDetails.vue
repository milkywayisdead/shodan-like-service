<template>
<complex-filter-info v-if="filterIsComplex" class="mb-2" />

<h3>
{{ locale.search.details }}
</h3>
<span v-if="maxItemsExceeded">
    ({{ locale.messages.first100Shown }}
    <v-tooltip :text="locale.messages.first100Cause">
      <template v-slot:activator="{ props }">
        <v-icon icon="mdi-information" v-bind="props" />)
      </template>
    </v-tooltip>
</span>

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
            facet: 'port'
        }
    },
    mixins: [detailsMixin],
}
</script>