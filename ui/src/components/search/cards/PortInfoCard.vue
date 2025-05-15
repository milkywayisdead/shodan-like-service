<template>
<v-card :id="`port_${info.port}`" style="scroll-margin-top:50px;"
    :title="`${info.port}`">
    <v-card-text>
        <p v-if="info.title" style="font-size:1rem;font-weight:600">{{ info.title }}</p>
        
        <div v-if="body.length" class="pl-0 pt-2 mt-2">
            <p v-for="(el, index) in body">
                {{ el }}
            </p>
        </div>

        <div v-if="headers.length" class="v-card-subtitle pl-0 pt-2 mt-2">
            <p v-for="(header, index) in headers">
                {{ header }}
            </p>
        </div>
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
            _mainParams: [
                //{title: 'port', value: 'port'},
                /*{title: 'service', value: 'service'},
                {title: 'software', value: 'software'},
                {title: 'application', value: 'application'},
                {title: 'component', value: 'component'},*/
                {title: 'title', value: 'title'},
                {title: 'headers', value: 'headers'},
                {title: 'body', value: 'body'},
            ]
        }
    },
    computed: {
        mainParams(){
            return this._mainParams.filter(
                item => this.info[item.value] !== ''
            )
        },
        headers(){
            const headers = this.info.headers
            if(!headers) return headers
            return headers.split('\r\n')
        },
        body(){
            const body = this.info.body
            if(!body) return body
            return body.split('\n')
        }
    },
    mounted(){
        if(!this.$route.hash) return

        const dId = `port_${this.info.port}`
        if(this.$route.hash.replace('#', '') === dId){
            document.getElementById(dId).scrollIntoView({behavior: 'smooth'})
        }
    }
}
</script>