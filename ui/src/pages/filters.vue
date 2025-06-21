<template>
<h1>{{ locale.nav.filters }}</h1>
<v-row>
    <v-col cols="3" v-for="(item, idx) in filters" :key="idx">
        <v-card flat :title="item.code" :subtitle="item.name">
            <v-card-text>{{ item.description }}</v-card-text>
        </v-card>   
    </v-col>
</v-row>
</template>

<script>
import { storeMixin } from '@/mixins/store';
import { miscApi } from '@/api/api.js'

export default {
    mixins: [storeMixin],
    data(){
        return {
            filters: []
        }
    },
    methods: {
        getFilters(){
            miscApi.getContent('filters')
                .then(res => {
                    this.filters = res.data.data
                })
        },
    },
    mounted(){
        this.getFilters()
    }
}
</script>

<route lang="yaml">
meta:
    layout: base
</route>