<template>
<search-results-domain-block :info="info" />
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