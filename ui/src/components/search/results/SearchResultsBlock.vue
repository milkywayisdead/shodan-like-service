<template>
<v-row>
    <v-col cols="2">
        <v-row>
            <v-col>
                <search-results-card 
                    :title="locale.search.results.totalResults" 
                    :totals="totals" />
            </v-col>
        </v-row>
        <v-row v-for="top in topCats">
            <v-col>
                <component 
                    :is="`Top${top.title}Card`" 
                    :title="locale.search.results[`top${top.title}`]"
                    :top-data="tops[top.key]" />
            </v-col>
        </v-row>
    </v-col>
    <v-col cols="10">
        <v-row v-for="host in hosts" :key="host.address">
            <v-col cols="6">
                <host-info-card 
                    :info="host"
                    :host-link="hostLink" 
                    @click="emitHostClicked(host)" />
            </v-col>
            <v-col cols="6">
                <ports-list-card :ports="host.total_ports" />
            </v-col>
        </v-row>
    </v-col>
</v-row>
</template>

<script>
import { storeMixin } from '@/mixins/store';
import TopAppsCard from '../cards/TopAppsCard.vue';
import TopPortsCard from '../cards/TopPortsCard.vue';
import TopServicesCard from '../cards/TopServicesCard.vue';
import TopComponentsCard from '../cards/TopComponentsCard.vue';
import TopSoftCard from '../cards/TopSoftCard.vue';

export default {
    mixins: [storeMixin,],
    emits: ['host-clicked'],
    props: {
        hosts: Array,
        tops: Object,
        totals: Object,
        hostLink: {
            type: Boolean,
            default: true
        },
    },
    data(){
        return {
            topCats: [
                {title: 'Ports', key: 'top_ports'}, 
                {title: 'Services', key: 'top_services'},
                {title: 'Soft', key: 'top_software'}, 
                {title: 'Apps', key: 'top_applications'},
                {title: 'Components', key: 'top_components'}
            ],
            page: 1,
            totalVisible: 5,
        }
    },
    methods: {
        emitHostClicked(host){
            this.$emit('host-clicked', JSON.parse(JSON.stringify(host)))
        }
    },
    components: {
        TopAppsCard,
        TopPortsCard,
        TopServicesCard,
        TopSoftCard,
        TopComponentsCard,
    }
}
</script>