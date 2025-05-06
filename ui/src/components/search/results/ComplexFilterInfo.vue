<template>
<v-chip
    color="primary"
    variant="outlined"
    prepend-icon="mdi-filter-plus"
    :closable="closable"
    @click:close="$emit('close')">
    {{ extraFilter.extraType }}: {{ extraFilter.extraQuery }}
</v-chip>
</template>

<script>
import { storeMixin } from '@/mixins/store';

export default {
    mixins: [storeMixin,],
    emits: ['close'],
    props: {
        closable: Boolean,
    },
    computed: {
        extraFilter(){
            const query = this.$route.query
            return {
                extraType: query.et,
                extraQuery: query.eq
            }
        }
    }
}
</script>