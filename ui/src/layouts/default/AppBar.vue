<template>
<v-app-bar density="compact">
    <v-spacer></v-spacer>
    <v-btn @click="$router.push('/register')">{{ locale.register }}</v-btn>
    <v-btn @click="$router.push('/login')">{{ locale.login }}</v-btn>
</v-app-bar>
</template>

<script>
import { useAppStore } from '@/stores/app';

export default {
    data(){
        return {
            locale: useAppStore().locale,
        }
    },
}
</script>