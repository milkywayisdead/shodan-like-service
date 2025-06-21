<template>
<h1>{{ locale.nav.feed }}</h1>
<v-row>
    <v-col cols="3" v-for="(item, idx) in news" :key="idx">
       <v-card flat>
            <v-card-title @click="toArticle(item.id)" class="clickable-element">{{ item.title }}</v-card-title>
            <v-card-subtitle>{{ new Date(item.created).toLocaleString() }}</v-card-subtitle>
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
            news: []
        }
    },
    methods: {
        getNews(){
            miscApi.getContent('news')
                .then(res => {
                    this.news = res.data.data
                })
        },
        toArticle(id){
            this.$router.push(`/feed/${id}`)
        }
    },
    mounted(){
        this.getNews()
    }
}
</script>

<route lang="yaml">
meta:
    layout: base
</route>