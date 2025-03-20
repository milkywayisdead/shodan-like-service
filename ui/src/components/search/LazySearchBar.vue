<template>
<v-row>
    <v-col cols="12">
        <v-text-field 
            v-model="search"
            density="compact"
            prepend-inner-icon="mdi-magnify"
            :placeholder="locale.search.placeholder"
            @keyup.enter="go">
            <template v-slot:prepend>
                <search-bar-menu ref="menu"
                    @change="searchType = $event"/>
            </template>
            <template v-slot:append="{ props }">
                <v-btn @click="go" :disabled="!search">{{ locale.search.search }}</v-btn>
            </template>
        </v-text-field>
    </v-col>
</v-row>    
</template>

<script>
import { storeMixin } from '@/mixins/store';

export default {
    mixins: [storeMixin],
    data(){
        return {
            search: '',
            searchType: '',
        }
    },
    methods: {
        go(){
            if(!this.search) return
            this.store.setSearchTerm(this.search)
            this.store.setSearchType(this.searchType)
            this.$router.push(`/search`)
        },
    },
    watch: {
        searchType(value){
            this.$refs.menu.setSearchTypeTitle(value)
        }
    },
    mounted(){
        //this.search = this.store.searchTerm
    }
}
</script>