<template>
<v-card 
    :title="title" 
    :height="height">
    <v-card-text>
        <p v-for="item in items">{{ item.title }}</p>
    </v-card-text>
</v-card>
</template>

<script>
import { storeMixin } from '@/mixins/store';

export default {
    props: {
        title: String,
        height: {
            type: Number,
            default: 100
        },
        items: Array,
    },
    mixins: [storeMixin,],
}
</script>