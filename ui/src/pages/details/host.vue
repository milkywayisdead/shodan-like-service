<template>
<lazy-search-bar />
<hosts-search-results :info="info" v-if="info"/>
</template>

<script>
import { storeMixin } from '@/mixins/store';
import { authMixin } from '@/mixins/auth';

export default {
    mixins: [storeMixin, authMixin],
    data(){
        return {
            info: null,
        }
    },
    methods: {
        setHostDetails(){
            this.info = {host: this.store.hostDetails}
        }
    },
    activated(){
        this.setHostDetails()
    },
    deactivated(){
        this.store.resetHostDetails()
    }
}
</script>

<route lang="yaml">
meta:
    layout: search
</route>