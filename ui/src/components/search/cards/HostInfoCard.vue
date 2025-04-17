<template>
<v-card>
    <v-card-title>
        {{ locale.search.results.main }}
        <v-btn v-if="hostLink" 
            icon="mdi-arrow-right" 
            @click="emitClick" 
            size="x-small" />
    </v-card-title>
    <v-card-text>
        <p v-for="param in mainParams" :key="param.value">
            {{ locale.host[param.title] }}: {{ info[param.value] }}
        </p>
        <p v-if="location.country">{{ locale.host.country }}: {{ location.country }}</p>
        <p v-if="location.city">{{ locale.host.city }}: {{ location.city }}</p>
    </v-card-text>
</v-card>
</template>

<script>
import { storeMixin } from '@/mixins/store';

export default {
    mixins: [storeMixin],
    emits: ['click'],
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
        hostLink: Boolean,
    },
    data(){
        return {
            _mainParams: [
                {title: 'host', value: 'IP'},
                {title: 'domain', value: 'domain'},
                //{title: 'location', value: 'Location'},
                {title: 'organization', value: 'Organization'},
                {title: 'asn', value: 'ASN'},
                {title: 'os', value: 'OS'},
                {title: 'net', value: 'net'},
            ]
        }
    },
    computed: {
        location(){
            const loc = this.info?.Location || []
            if(!loc.length){
                return {city: '', country: ''}
            }
            return loc[0]
        },
        mainParams(){
            return this._mainParams.filter(
                item => this.info[item.value] !== ''
            )
        }
    },
    methods: {
        emitClick(){
            this.$emit('click')
        }
    }
}
</script>