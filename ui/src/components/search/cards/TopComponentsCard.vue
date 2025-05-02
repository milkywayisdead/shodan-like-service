<template>
<v-card 
    :title="locale.search.results.topServices" >
    <v-card-text>
        <p v-for="data in items" 
            :key="data._id"
            class="clickable-element"
            @click="emitExtendSearch(extendedSearch(data._id))">
            {{ data._id }}: {{ data.count }}
        </p>
        <a v-if="showMore" class="nodecor"
            @click.prevent="toMore"
            href="">
            {{ locale.search.more }}...
        </a>
    </v-card-text>
</v-card>
</template>

<script>
import { storeMixin } from '@/mixins/store';
import { topsMixin, searchJumpMixin } from '@/mixins/search';

export default {
    mixins: [storeMixin, topsMixin, searchJumpMixin],
    props: {
        topData: Array,
    },
    data(){
        return {
            type: 'component'
        }
    }
}
</script>