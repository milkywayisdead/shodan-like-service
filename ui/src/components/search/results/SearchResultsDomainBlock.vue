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
        <v-row>
            <v-col cols="12">
                <div>info</div>
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
import { storeMixin } from '@/mixins/store';
import { useAppStore } from '@/stores/app';
import TopAppsCard from '../cards/TopAppsCard.vue';
import TopPortsCard from '../cards/TopPortsCard.vue';
import TopServicesCard from '../cards/TopServicesCard.vue';
import TopComponentsCard from '../cards/TopComponentsCard.vue';
import TopSoftCard from '../cards/TopSoftCard.vue';

export default {
    mixins: [storeMixin],
    props: {
        info: {
            type: Object,
            default: {}
        },
        tops: Object,
        totals: Object,
    },
    data(){
        const locale = useAppStore().locale
        return {
            tableHeaders: [
                {title: locale.domain.name, key: 'name'},
                {title: locale.domain.type, key: 'type'},
                {title: locale.domain.value, key: 'value'},
            ],
            domainInfo: [],
            topCats: [
                {title: 'Ports', key: 'top_ports'}, 
                {title: 'Services', key: 'top_services'},
                {title: 'Soft', key: 'top_software'}, 
                {title: 'Apps', key: 'top_applications'},
                {title: 'Components', key: 'top_components'}
            ],
        }
    },
    mounted(){
        for(let i=0;i<11;i++){
            this.domainInfo.push({name: 'some.domain.org', type: 'A', value: '1.1.1.1'})
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