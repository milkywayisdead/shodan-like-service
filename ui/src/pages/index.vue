<template>
    <v-row>
        <v-col cols="3" v-for="card in cards">
            <v-card :title="`Функционал ${card}`" :height="400"></v-card>
        </v-col>
    </v-row>
    <v-row>
        <v-col cols="12">
            <v-card title="Новость" :height="100"></v-card>
        </v-col>
    </v-row>
</template>

<script>
import { useAuthStore } from '../stores/auth.js'
import { useRouter } from 'vue-router'
import { useAppStore } from '@/stores/app.js'

export default {
    setup() {
        const authStore = useAuthStore()
        const router = useRouter()
        const storage = useAppStore()

        return {
            authStore,
            router,
            locale: storage.locale,
            cards: [1, 2, 3, 4]
        }
    },
    methods: {
        async logout() {
            try {
                await this.authStore.logout(this.$router)
            } catch (error) {
                console.error(error)
            }
        }
    },
    async mounted() {
        await this.authStore.fetchUser()
    }
}
</script>

<route lang="yaml">
meta:
    layout: base
</route>