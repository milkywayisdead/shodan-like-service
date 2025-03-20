<template>
<v-row>
    <v-col cols="2">
        <v-row>
            <v-col>
                <search-results-card :title="locale.search.results.totalResults" />
            </v-col>
        </v-row>
        <v-row v-for="top in tops">
            <v-col>
                <search-results-card :title="locale.search.results[`top${top}`]" />
            </v-col>
        </v-row>
    </v-col>
    <v-col cols="4">
        <v-row v-for="dummy in dummies" :key="dummy">
            <v-col>
                <search-results-card :title="locale.search.host + ` ${dummy}`" />
            </v-col>
        </v-row>
    </v-col>
    <v-col cols="6">
        <v-row v-for="dummy in dummies" :key="dummy">
            <v-col>
                <search-results-card :title="locale.search.results.portDetails + ` ${dummy}`" />
            </v-col>
        </v-row>
    </v-col>
</v-row>
<v-pagination
    v-model="page" 
    :length="paginationLength" 
    :total-visible="totalVisible" />
</template>

<script>
import { useAppStore } from '@/stores/app';

export default {
    data(){
        return {
            locale: useAppStore().locale,
            _dummies: [1,2,3,4,5,6,7,8,9,10],
            tops: ['Ports', 'Services', 'Apps', 'Components'],
            page: 1,
            totalVisible: 5,
            paginationLength: 50,
        }
    },
    computed: {
        dummies(){
            return this._dummies.map(i => (this.page - 1)*10 + i)
        }
    }
}
</script>