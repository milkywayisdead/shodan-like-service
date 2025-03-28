<template>
<v-main>
    <sidebar />
    <app-bar v-if="!authStore.isAuthenticated" />
    <v-container>
        <router-view v-slot="{Component}">
            <keep-alive>
                <component :is="Component" />
            </keep-alive>
        </router-view>
        <loader-overlay :loading="store.loading" />
    </v-container>
</v-main>
<app-footer />
</template>

<script setup>
import Sidebar from './default/Sidebar.vue';
import AppBar from './default/AppBar.vue';
import AppFooter from './default/AppFooter.vue';
import { useAuthStore } from '@/stores/auth';
import { useAppStore } from '@/stores/app';

const authStore = useAuthStore()
const store = useAppStore()
</script>
