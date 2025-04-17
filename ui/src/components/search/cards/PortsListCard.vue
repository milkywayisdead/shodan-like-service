<template>
<v-card 
    :title="locale.search.results.openPorts">
    <v-card-text>
        <p v-if="!ports.length">{{ locale.search.noResults }}</p>
        <v-chip class="mr-1" v-if="ports.length"
            v-for="port in ports" 
            :key="port.port"
            label>
            {{ port.port }}
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
    },
}
</script>