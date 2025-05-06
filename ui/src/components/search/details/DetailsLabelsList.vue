<template>
<p v-for="(label, index) in labels"
    style="height:42px;padding-top:13px;"
    :key="index">
    <span class="clickable-element" @click="emitClick(label)">{{ label }}</span>
</p>
</template>

<script>
export default {
    props: {
        labels: Array,
    },
    emits: ['click'],
    methods: {
        emitClick(item){
            this.$emit('click', item)
        }
    }
}
</script>