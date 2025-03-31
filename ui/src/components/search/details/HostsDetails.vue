<template>
<hosts-search-results-details v-if="info"
    :info="info"
    host-link />
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
        setDetails(){
            this.info = {host: this.store.hostDetails}
        },
    },
}
</script>