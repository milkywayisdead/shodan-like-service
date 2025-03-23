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
    emits: ['search'],
    methods: {
        go(){
            if(!this.search) return
            const term = this.search.trim()
            this.search = term
            this.store.setSearchTerm(term)
            this.$emit('search', {term: term, type: this.searchType})
        },
    },
    watch: {
        searchType(value){
            this.$refs.menu.setSearchTypeTitle(value)
        }
    },
    mounted(){
        this.search = this.store.searchTerm
        this.searchType = this.store.searchType
        this.go()
    }
}
</script>