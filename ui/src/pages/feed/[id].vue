<template>
<v-row v-if="item">
    <v-col cols="12">
        <v-card flat :title="item.title" :subtitle="new Date(item.created).toLocaleString()">
            <v-card-text>{{ item.full_text }}</v-card-text>
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
            item: null
        }
    },
    methods: {
        getArticle(){
            miscApi.getContentItem('news', this.$route.params.id)
                .then(res => {
                    this.item = res.data.data
                })
        },
    },
    mounted(){
        this.getArticle()
    }
}
</script>

<route lang="yaml">
meta:
    layout: base
</route>