<template>
<v-alert 
    color="info"
    icon="$info"
    variant="tonal" :title="locale.search.noResults" />
</template>

<script>
import { storeMixin } from '@/mixins/store';

export default {
    mixins: [storeMixin,]
}
</script>