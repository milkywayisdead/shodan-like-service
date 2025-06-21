<template>

<v-row>
    <v-col cols="12">
        <v-card title="Функционал" height="auto">
            <v-card-text>
                <v-row>
                    <v-col cols="3" v-for="(item, idx) in functionality" :key="idx">
                        <v-card flat :title="item.name">
                            <v-card-text>{{ item.description }}</v-card-text>
                        </v-card>   
                    </v-col>
                </v-row>
            </v-card-text>
        </v-card>
    </v-col>
</v-row>
<v-row>
    <v-col cols="12">
        <v-card title="Новости" height="auto">
            <v-card-text>
                <v-row>
                    <v-col cols="3" v-for="(item, idx) in news" :key="idx">
                        <v-card flat :title="item.title">
                            <v-card-text>{{ item.description }}</v-card-text>
                        </v-card>   
                    </v-col>
                </v-row>
            </v-card-text>
        </v-card>
    </v-col>
</v-row>
</template>

<script>
import { useAuthStore } from '../stores/auth.js'
import { useRouter } from 'vue-router'
import { useAppStore } from '@/stores/app.js'
import { miscApi } from '@/api/api.js'
import { ref } from 'vue'

export default {
    setup() {
        const authStore = useAuthStore()
        const router = useRouter()
        const storage = useAppStore()

        return {
            authStore,
            router,
            locale: storage.locale,
            news: ref([]),
            functionality: ref([])
        }
    },
    methods: {
        async logout() {
            try {
                await this.authStore.logout(this.$router)
            } catch (error) {
                console.error(error)
            }
        },
        getNews(){
            miscApi.getContent('news')
                .then(res => {
                    this.news = res.data.data
                })
        },
        getFunctionality(){
            miscApi.getContent('functionality')
                .then(res => {
                    this.functionality = res.data.data
                    console.log(this.functionality)
                })
        },
    },
    async mounted() {
        await this.authStore.fetchUser()

        this.getNews()
        this.getFunctionality()
    }
}
</script>

<route lang="yaml">
meta:
    layout: base
</route>