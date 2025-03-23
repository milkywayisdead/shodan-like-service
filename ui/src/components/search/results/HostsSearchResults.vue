<template>
<v-row v-if="info.host">
    <v-col cols="6">
        <v-row>
            <v-col>
                <host-info-card :info="info.host" />
            </v-col>
        </v-row>
        <v-row>
            <v-col v-if="info.soft">
                <search-results-card :title="locale.search.results.soft" />
            </v-col>
        </v-row>
        <v-row>
            <v-col v-if="info.apps">
                <search-results-card :title="locale.search.results.apps" />
            </v-col>
        </v-row>
        <v-row>
            <v-col v-if="info.components">
                <search-results-card :title="locale.search.results.components" />
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
        }
    }
}
</script>