<template>
<v-card 
    :title="locale.search.results.openPorts">
    <v-card-text>
        <v-chip class="mr-1" v-if="clickable"
            v-for="port in portsSlice" 
            :key="port.port"
            label
            color="primary"
            @click="emitClick"
            variant="flat">
            {{ portLabel(port.port) }}
        </v-chip>
        <v-chip class="mr-1" v-if="!clickable"
            v-for="port in portsSlice" 
            :key="port.port"
            color="primary"
            label
            variant="flat">
            {{ portLabel(port.port) }}
        </v-chip>
    </v-card-text>
</v-card>
</template>

<script>
import { storeMixin } from '@/mixins/store';

export default {
    mixins: [storeMixin],
    props: {
        title: String,
        height: {
            type: Number,
            default: 100
        },
        ports: {
            type: Array,
        },
        clickable: Boolean,
    },
    emits: ['click'],
    methods: {
        portLabel(port){
            return port === 'more' ? this.locale.more : port
        },
        emitClick(){
            this.$emit('click')
        }
    },
    computed: {
        portsSlice(){
            const N = 20
            const l = this.ports.length
            if(l >= N){
                const slice = this.ports.slice(0, N-1)
                slice.push({port: 'more'})
                return slice
            } else {
                return this.ports
            }
        }
    }
}
</script>