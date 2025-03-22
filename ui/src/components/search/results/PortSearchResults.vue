<template>
    <search-results-block 
        :hosts="info.hosts || []" 
        :tops="info.tops[0] || {}" />
    </template>

<script>
export default {
    props: {
        info: {
            type: Object,
            default: {}
        }
    },
}
</script>