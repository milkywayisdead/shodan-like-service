<template>
<v-navigation-drawer
    v-model="drawer"
    :rail="rail"
    permanent
    >
    <v-list-item nav>
        <h1>Service</h1>
        <template v-slot:append>
            <v-btn
                icon="mdi-spider-thread"
                variant="text"
                @click.stop="rail = !rail"
            ></v-btn>
        </template>
    </v-list-item>

    <v-divider></v-divider>

    <v-list density="compact" nav>
        <v-list-item link v-for="item in items" 
            :key="item.value" 
            :prepend-icon="item.icon" 
            :title="item.title" 
            :value="item.value"
            :to="item.to">
        </v-list-item>
    </v-list>

    <template v-slot:append>
        <v-list density="compact" nav>
            <v-list-item v-for="item in itemsToAppend" 
                :key="item.value" 
                :prepend-icon="item.icon" 
                :title="item.title" 
                :value="item.value"
                :to="item.to">
            </v-list-item>
            <v-list-item v-if="auth.isAuthenticated">
                <v-btn @click="auth.logout($router, setLoading, resetLoading)">{{ locale.signOut }}</v-btn>
            </v-list-item>
        </v-list>
    </template>
</v-navigation-drawer>
</template>

<script>
import { useAuthStore } from '@/stores/auth';
import { storeMixin } from '@/mixins/store';

export default {
    mixins: [storeMixin],
    data(){
        return {
            rail: true,
            drawer: null,
            auth: useAuthStore(),
        }
    },
    computed: {
        items(){
            const nav = this.locale.nav
            const items = [
                {title: nav.feed, icon: 'mdi-rss', value: 'feed', to: '/feed'},
                {title: nav.tools, icon: 'mdi-tools', value: 'tools', to: '/tools'},
                {title: nav.filters, icon: 'mdi-filter', value: 'filters', to: '/filters'},
            ]
            if(this.auth.isAuthenticated){
                items.unshift({title: nav.dashboard, icon: 'mdi-view-dashboard', value: 'dashboard', to: '/dashboard'})
            } else {
                items.unshift({title: nav.home, icon: 'mdi-home', value: 'index', to: '/'},)
            }
            return items
        },
        itemsToAppend(){
            let items = []
            const nav = this.locale.nav
            if(this.auth.isAuthenticated){
                items = [
                    {title: nav.account, icon: 'mdi-account', value: 'account', to: '/account'},
                    {title: nav.notifications, icon: 'mdi-bell', value: 'notifications', to: '/notifications'},
                ]
            }
            items.push({title: nav.help, icon: 'mdi-help-box-outline', value: 'help', to: '/help'})
            return items
        },
        setLoading(){
            this.store.loading = true
        },
        resetLoading(){
            setTimeout(() => {
                this.store.loading = false
            }, 500)
        }
    }
}
</script>