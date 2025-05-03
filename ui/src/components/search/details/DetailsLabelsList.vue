<template>
<p v-for="(label, index) in labels"
    style="height:50px;padding-top:17px;margin-bottom:5px"
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