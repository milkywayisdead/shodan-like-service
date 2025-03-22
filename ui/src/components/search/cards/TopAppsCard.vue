<template>
<v-card 
    :title="locale.search.results.topApps" >
    <v-card-text>
    </v-card-text>
</v-card>
</template>

<script>
import { storeMixin } from '@/mixins/store';

export default {
    mixins: [storeMixin],
    props: {
        topData: Array,
    }
}
</script>