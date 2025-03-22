<template>
<v-card 
    :title="title" 
    :height="height">
    <v-card-text>
        <p>{{ locale.search.results.hostsTotal }}: {{ totals.hosts }}</p>
        <p>{{ locale.search.results.portsTotal }}: {{ totals.ports }}</p>
    </v-card-text>
</v-card>
</template>

<script>
import { storeMixin } from '@/mixins/store';

export default {
    props: {
        title: String,
        height: {
            type: Number,
            default: 100
        },
        totals: {
            type: Object,
        }
    },
    mixins: [storeMixin,],
}
</script>