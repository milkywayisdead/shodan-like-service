<template>
<v-text-field v-if="type === 'text'" />
</template>

<script>
export default {
    props: {
        type: String,
    },
}
</script>