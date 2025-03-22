<template>
<v-row>
    <v-col cols="2">
        <v-row>
            <v-col>
                <search-results-card :title="locale.search.results.totalResults" />
            </v-col>
        </v-row>
        <v-row v-for="top in topCats">
            <v-col>
                <search-results-card :title="locale.search.results[`top${top}`]" />
            </v-col>
        </v-row>
    </v-col>
    <v-col cols="10">
        <v-row v-for="host in hosts" :key="host.address">
            <v-col cols="5">
                <host-info-card :info="host" />
            </v-col>
            <v-col cols="7">
                <ports-list-card :ports="host.total_ports" />
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
import { storeMixin } from '@/mixins/store';

export default {
    mixins: [storeMixin],
    props: {
        hosts: Array,
        tops: Object,
    },
    data(){
        return {
            topCats: ['Ports', 'Services', 'Apps', 'Components'],
            page: 1,
            totalVisible: 5,
            paginationLength: 50,
        }
    },
}
</script>