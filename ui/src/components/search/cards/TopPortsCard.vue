<template>
<v-card 
    :title="locale.search.results.topPorts" >
    <v-card-text>
        <p v-for="data in topData" :key="data._id">
            {{ data._id }}: {{ data.count }}
        </p>
        <p>
            <a @click="toMore">{{ locale.search.more }}...</a>
        </p>
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