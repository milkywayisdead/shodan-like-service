<template>
<h1></h1>
<v-navigation-drawer permanent>
    <v-list>
        <v-list-item v-for="item in sideMenuItems" 
            :key="item.value"
            :value="item.value"
            :title="item.title"></v-list-item>
    </v-list>
</v-navigation-drawer> 
</template>

<script>
import { useAppStore } from '@/stores/app';

export default {
    data(){
        const locale = useAppStore().locale
        return {
            sideMenuItems: [
                {title: locale.account.profile, value: 'profile'},
                {title: locale.account.history, value: 'history'},
                {title: locale.account.notifications, value: 'notifications'},
                {title: locale.account.api, value: 'api'},
            ]
        }
    }
}
</script>

<route lang="yaml">
meta:
    layout: account
    authRequired: true
</route>