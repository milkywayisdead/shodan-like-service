<template>
<h3>{{ locale.search.details }}</h3>
<v-row>
    <v-col cols="2" style="padding-top:25px">
        <details-labels-list 
            :labels="labels"
            @click="extendedSearch" />
    </v-col>
    <v-col cols="10">
        <bar-chart v-if="labels.length"
            :chart-data="chartData" 
            :height="chartHeight" />
    </v-col>
</v-row>
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