<template>
<v-row>
    <v-col cols="12">
        <v-text-field 
            v-model="search"
            density="compact"
            prepend-inner-icon="mdi-magnify"
            :placeholder="locale.search.placeholder"
            @keyup.enter="go"
            :disabled="locked">
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
    data(){
        return {
            search: '',
            searchType: '',
        }
    },
    emits: ['search'],
    methods: {
        go(){
            const term = this.search.trim()
            if(!term || !this.searchType || !this.btnEnabled) return
            this.search = term

            const query = this.$route.query
            const t = query.t || ''
            const q = query.q || ''
            if(t === this.searchType && q === term){
                this.$emit('search', {q, t})
            }

            this.$router.push(`/search?t=${this.searchType}&q=${term}`)
        },
        setTypeAndTerm(type, term){
            this.search = term
            this.searchType = type
            this.$refs.menu.setSearchTypeTitle(type)
        }
    },
    computed: {
        btnEnabled(){
            if(this.locked) return false
            const rule = searchRules[this.searchType]
            if(rule){
                return rule(this.search)
            }
            return false
        },
        locked(){
            return this.store.loading
        }
    },
}
</script>