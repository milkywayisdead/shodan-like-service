<template>
<v-card 
    :title="locale.search.results.apps">
    <v-card-text>
        <p  v-for="item in items"
            class="clickable-element"
            @click="emitParamClickedOrIgnore('app', item.title)">
            {{ item.title }}
        </p>
    </v-card-text>
</v-card>
</template>

<script>
import { storeMixin } from '@/mixins/store';
import { searchFacetMixin } from '@/mixins/search';

export default {
    props: {
        height: {
            type: Number,
            default: 100
        },
        items: Array,
    },
    mixins: [storeMixin, searchFacetMixin],
}
</script>