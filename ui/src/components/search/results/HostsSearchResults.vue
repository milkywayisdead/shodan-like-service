<template>
<v-row v-if="info.host">
    <v-col cols="6">
        <v-row>
            <v-col>
                <host-info-card 
                    :info="info.host" 
                    @facet-clicked="emitSearchBy" />
            </v-col>
        </v-row>
        <v-row>
            <v-col v-if="softList.length">
                <search-results-soft 
                    :items="softList" 
                    @facet-clicked="emitSearchBy" />
            </v-col>
        </v-row>
        <v-row>
            <v-col v-if="appsList.length">
                <search-results-apps
                    :items="appsList" 
                    @facet-clicked="emitSearchBy" />
            </v-col>
        </v-row>
        <v-row>
            <v-col v-if="componentsList.length">
                <search-results-components
                    :items="componentsList" 
                    @facet-clicked="emitSearchBy" />
            </v-col>
        </v-row>
    </v-col>
    <v-col cols="6">
        <v-row>
            <v-col>
                <ports-list-card :ports="portsList" />
            </v-col>
        </v-row>
        <v-row v-for="port in filteredPortsList" :key="port.port">
            <v-col>
                <port-info-card :info="port" />
            </v-col>
        </v-row>
    </v-col>
</v-row>
</template>

<script>
import { storeMixin } from '@/mixins/store';
import { searchJumpMixin } from '@/mixins/search';

const portParams = ['title', 'headers', 'body']


export default {
    mixins: [storeMixin, searchJumpMixin],
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
        filteredPortsList(){
            return this.portsList.filter(port => {
                let include = false
                for(let param of portParams){
                    if(port[param]){
                        include = true
                        break
                    }
                }
                return include
            })
        },
        appsList(){
            const arr = []
            for(let item of this.portsList){
                if(item.application){
                    arr.push({title: item.application})
                }
            }
            return Array.from(new Set(arr))
        },
        componentsList(){
            const arr = []
            for(let item of this.portsList){
                if(item.component){
                    arr.push({title: item.component})
                }
            }
            return Array.from(new Set(arr))
        },
        softList(){
            const arr = []
            for(let item of this.portsList){
                if(item.software){
                    arr.push({title: item.software})
                }
            }
            return Array.from(new Set(arr))
        }
    }
}
</script>