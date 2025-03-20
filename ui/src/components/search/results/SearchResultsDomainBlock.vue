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
    <v-col cols="10">
        <v-row>
            <v-col cols="12">
                <search-results-card title="Инфо о домене" />
            </v-col>
        </v-row>
        <v-row>
            <v-col cols="12">
                <custom-table :headers="tableHeaders" :items="domainInfo" />
            </v-col>
        </v-row>
    </v-col>
</v-row>
</template>

<script>
import { useAppStore } from '@/stores/app';

export default {
    data(){
        const locale = useAppStore().locale
        return {
            locale: locale,
            tops: ['Ports', 'Services', 'Apps', 'Components'],
            tableHeaders: [
                {title: locale.domain.name, key: 'name'},
                {title: locale.domain.type, key: 'type'},
                {title: locale.domain.value, key: 'value'},
            ],
            domainInfo: []
        }
    },
    mounted(){
        for(let i=0;i<11;i++){
            this.domainInfo.push({name: 'some.domain.org', type: 'A', value: '1.1.1.1'})
        }
    }
}
</script>