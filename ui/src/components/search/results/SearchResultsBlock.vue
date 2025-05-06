<template>
<v-row>
    <v-col cols="3">
        <v-row>
            <v-col>
                <search-results-card 
                    :title="locale.search.results.totalResults" 
                    :totals="totals" 
                    :show-ports="!portResults" />
            </v-col>
        </v-row>
        <v-row v-for="top in topCats">
            <v-col>
                <component 
                    :is="`Top${top.title}Card`" 
                    :title="locale.search.results[`top${top.title}`]"
                    :top-data="tops[top.key]" 
                    @extend-search="emitExtendSearch" />
            </v-col>
        </v-row>
    </v-col>
    <v-col cols="9">
        <v-row v-for="host in hosts" :key="host.address">
            <v-col cols="6">
                <host-info-card 
                    :info="host"
                    :host-link="hostLink" 
                    @click="emitHostClicked(host)" 
                    @facet-clicked="emitExtendSearch" />
            </v-col>
            <v-col cols="6">
                <ports-list-card
                    @click="emitHostClicked(host)"
                    :ports="host.total_ports" 
                    clickable />
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
import { searchJumpMixin } from '@/mixins/search';

export default {
    mixins: [storeMixin, searchJumpMixin],
    emits: ['host-clicked'],
    props: {
        hosts: Array,
        tops: Object,
        totals: Object,
        hostLink: {
            type: Boolean,
            default: true
        },
        portResults: Boolean,
    },
    data(){
        return {
            _topCats: [
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
    computed: {
        topCats(){
            let cats = this._topCats
            if(this.portResults){
                cats = cats.filter(cat => cat.key !== 'top_ports')
            }
            cats = cats.filter(cat => {
                return this.tops[cat.key].filter(item => {
                    return item._id !== ''
                }).length > 0
            })
            return cats
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