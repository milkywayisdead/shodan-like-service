<template>
<v-data-table 
    :headers="headers"
    :items="items" />    
</template>

<script>
export default {
    props: {
        headers: Array,
        items: Array
    }
}
</script>