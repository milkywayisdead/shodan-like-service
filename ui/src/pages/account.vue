<template>
<h1></h1>
<v-navigation-drawer permanent>
    <v-list v-model:selected="selected">
        <v-list-item v-for="item in sideMenuItems" 
            :key="item.value"
            :value="item.value"
            :title="item.title"></v-list-item>
    </v-list>
</v-navigation-drawer>
<component :is="`user-${tab}`" />
</template>

<script>
import { useAppStore } from '@/stores/app';
import { storeMixin } from '@/mixins/store'
import { useAuthStore } from '../stores/auth.js'
import UserProfile from '@/components/account/UserProfile.vue'
import UserEmail from '@/components/account/UserEmail.vue'
import UserPassword from '@/components/account/UserPassword.vue'

export default {
    mixins: [storeMixin],
    data(){
        const locale = useAppStore().locale
        return {
            sideMenuItems: [
                {title: locale.account.profile, value: 'profile'},
                {title: locale.account.email, value: 'email'},
                {title: locale.account.password, value: 'password'},
                {title: locale.account.history, value: 'history'},
                {title: locale.account.notifications, value: 'notifications'},
                {title: locale.account.api, value: 'api'},
            ],
            selected: ['profile']
        }
    },
    computed: {
        tab(){
            return this.selected[0]
        }
    },
    components: {
        UserProfile,
        UserEmail,
        UserPassword,
    }
}
</script>

<route lang="yaml">
meta:
    layout: account
    authRequired: true
</route>