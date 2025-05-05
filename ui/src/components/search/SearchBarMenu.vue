<template>
<v-menu>
    <template v-slot:activator="{ props }">
        <v-btn append-icon="mdi-chevron-down" variant="text" v-bind="props">{{ searchTypeTitle }}</v-btn>
    </template>

    <v-list>
        <v-list-item
            v-for="(item, i) in searchTypes"
                :key="i"
                :value="i"
                @click="searchTypeTitle = item.title, $emit('change', item.value)"
            >
        <v-list-item-title>{{ item.title }}</v-list-item-title>
        </v-list-item>
    </v-list>
</v-menu>
</template>

<script>
import { useAuthStore } from '@/stores/auth';
import { useAppStore } from '@/stores/app';

export default {
    data(){
        return {
            auth: useAuthStore(),
            locale: useAppStore().locale,
            searchTypeTitle: 'Hosts'
        }
    },
    emits: ['change'],
    methods: {
        setSearchTypeTitle(type){
            this.searchTypeTitle = this.searchTypes.find(i => i.value === type)?.title || 'Hosts'
        }
    },
    computed: {
        searchTypes(){
            const searchLoc = this.locale.search
            const items = [
                {title: searchLoc.hosts, value: 'hosts'},
                {title: searchLoc.net, value: 'net'},
                {title: searchLoc.port, value: 'port'},
                {title: searchLoc.asn, value: 'asn'},
            ]
            if(this.auth.isAuthenticated){
                items.push(...[
                    {title: searchLoc.org, value: 'org'},
                    {title: searchLoc.city, value: 'city'},
                    {title: searchLoc.country, value: 'country'},
                    {title: searchLoc.domain, value: 'domain'},
                    {title: searchLoc.os, value: 'os'},
                    {title: searchLoc.service, value: 'service'},
                    {title: searchLoc.soft, value: 'soft'},
                    {title: searchLoc.app, value: 'app'},
                    {title: searchLoc.component, value: 'component'},
                ])
            }
            return items
        }
    },
    mounted(){
        this.$emit('change', this.searchTypes[0].value)
    }
}
</script>