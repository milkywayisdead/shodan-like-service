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
                <v-btn @click="go" :disabled="!btnEnabled">{{ locale.search.search }}</v-btn>
            </template>
        </v-text-field>
    </v-col>
</v-row>    
</template>

<script>
import { storeMixin } from '@/mixins/store';
import searchRules from '@/utils/searchRules';

export default {
    mixins: [storeMixin],
    props: {
        hostDetails: Boolean,
    },
    data(){
        return {
            search: '',
            searchType: '',
        }
    },
    methods: {
        go(){
            const term = this.search.trim()
            if(!term || !this.searchType || !this.btnEnabled) return
            this.search = term
            this.$router.push(`/search?t=${this.searchType}&q=${term}`)
        },
    },
    computed: {
        btnEnabled(){
            const rule = searchRules[this.searchType]
            if(rule){
                return rule(this.search)
            }
            return false
        }
    },
    watch: {
        searchType(value){
            this.$refs.menu.setSearchTypeTitle(value)
        }
    },
}
</script>