<template>
<v-footer density="compact" height="40" app color="surface-light">
    <v-btn
        v-for="link in links"
        :key="link.value"
        :text="link.title"
        variant="text"
        rounded
        @click="$router.push(link.to)"
    ></v-btn>
</v-footer>
</template>

<script setup>
import { useAppStore } from '@/stores/app';

const locale = useAppStore().locale

const links = [
    {title: locale.nav.home, to: '/', value: 'home'},
    {title: locale.nav.contacts, to: '/', value: 'contacts'},
    {title: locale.nav.feed, to: '/feed', value: 'home'},
]
</script>