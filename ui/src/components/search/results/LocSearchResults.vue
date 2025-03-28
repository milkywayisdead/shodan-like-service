<template>
<search-results-block 
    :hosts="info.hosts || []" 
    :tops="(info.tops || [])[0] || {}"
    :totals="totals" 
    @host-clicked="emitHostClicked($event)" />
</template>

<script>
import { genericResultsMixin } from '@/mixins/search';

export default {
    mixins: [genericResultsMixin],
}
</script>