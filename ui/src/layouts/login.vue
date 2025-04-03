<template>
<v-main>
    <sidebar />
    <v-container class="fill-height" fluid>
        <router-view />
        <loader-overlay :loading="store.loading" />
    </v-container>
    <snackbar-notif />
</v-main>
<app-footer />
</template>

<script setup>
import Sidebar from './default/Sidebar.vue';
import AppFooter from './default/AppFooter.vue';
import { useAuthStore } from '@/stores/auth';
import { useAppStore } from '@/stores/app';

const authStore = useAuthStore()
const store = useAppStore()
</script>
