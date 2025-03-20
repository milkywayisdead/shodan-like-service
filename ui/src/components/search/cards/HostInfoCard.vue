<template>
<v-card 
    :title="locale.search.results.main" >
    <v-card-text>
        <p v-for="param in mainParams" :key="param.value">
            {{ locale.host[param.title] }}: {{ info[param.value] }}
        </p>
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
        info: {
            type: Object,
            default: {}
        },
    },
    data(){
        return {
            mainParams: [
                {title: 'host', value: 'IP'},
                {title: 'domain', value: 'domain'},
                {title: 'location', value: 'Location'},
                {title: 'organization', value: 'Organization'},
                {title: 'asn', value: 'ASN'},
                {title: 'os', value: 'OS'},
                {title: 'net', value: 'Net'},
            ]
        }
    },
}
</script>