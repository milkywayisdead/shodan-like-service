<template>
<v-row v-if="info.host">
    <v-col cols="6">
        <v-row>
            <v-col>
                <host-info-card :info="info.host" />
            </v-col>
        </v-row>
        <v-row>
            <v-col v-if="softList.length">
                <search-results-asc 
                    :title="locale.search.results.soft" 
                    :items="softList" />
            </v-col>
        </v-row>
        <v-row>
            <v-col v-if="appsList.length">
                <search-results-asc 
                    :title="locale.search.results.apps" 
                    :items="appsList" />
            </v-col>
        </v-row>
        <v-row>
            <v-col v-if="componentsList.length">
                <search-results-asc 
                    :title="locale.search.results.components" 
                    :items="componentsList" />
            </v-col>
        </v-row>
    </v-col>
    <v-col cols="6">
        <v-row>
            <v-col>
                <ports-list-card :ports="portsList" />
            </v-col>
        </v-row>
        <v-row v-for="port in portsList" :key="port.port">
            <v-col>
                <port-info-card :info="port" />
            </v-col>
        </v-row>
    </v-col>
</v-row>
</template>

<script>
import { storeMixin } from '@/mixins/store';

export default {
    mixins: [storeMixin, ],
    props: {
        info: {
            type: Object,
            default: {}
        }
    },
    computed: {
        portsList(){
            return this.info?.host.total_ports || []
        },
        appsList(){
            return Array.from(new Set(this.portsList.map(item => ({title: item.application}))))
        },
        componentsList(){
            return Array.from(new Set(this.portsList.map(item => ({title: item.component}))))
        },
        softList(){
            return Array.from(new Set(this.portsList.map(item => ({title: item.software}))))
        }
    }
}
</script>