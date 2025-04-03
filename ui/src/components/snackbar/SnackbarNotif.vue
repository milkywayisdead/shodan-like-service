<template>
<div id="snackbars-container">
    <v-snackbar v-for="(item, index) in items"
        :key="item.id"
        :text="item.text"
        :timeout="5000"
        :model-value="item.visible"
        @update:model-value="deleteNotif(item.id)"
        location="bottom right"
        :color="item.color"
        :style="`bottom: ${index*50 + 4}px`">
        <template v-slot:actions>
            <v-btn icon="mdi-close" @click="deleteNotif(item.id)"></v-btn>
        </template>
    </v-snackbar>
</div>    
</template>

<script>
import { storeMixin } from '@/mixins/store';

export default {
    mixins: [storeMixin],
    computed: {
        items(){
            return this.store.notifs
        }
    },
    methods: {
        deleteNotif(id){
            this.store.deleteNotif(id)
        }
    },
}
</script>