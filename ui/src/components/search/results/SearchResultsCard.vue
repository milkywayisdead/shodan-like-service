<template>
<v-card :title="title" :height="height"></v-card>
</template>

<script>
export default {
    props: {
        title: String,
        height: {
            type: Number,
            default: 100
        }
    },
}
</script>