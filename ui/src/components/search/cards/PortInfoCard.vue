<template>
<v-card 
    :title="`${locale.search.results.port} ${info.port}`">
    <v-card-text>
        <p v-for="param in mainParams" :key="param.value">
            {{ locale.port[param.title] }}: {{ info[param.value] }}
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
                //{title: 'port', value: 'port'},
                {title: 'service', value: 'service'},
                {title: 'software', value: 'software'},
                {title: 'application', value: 'application'},
                {title: 'component', value: 'component'},
                {title: 'title', value: 'title'},
                {title: 'headers', value: 'headers'},
                {title: 'body', value: 'body'},
            ]
        }
    },
}
</script>