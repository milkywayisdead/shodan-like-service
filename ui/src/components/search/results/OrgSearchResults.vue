<template>
<search-results-block 
    :hosts="info.hosts || []" 
    :tops="(info.tops || [])[0] || {}"
    :totals="totals" 
    @host-clicked="emitHostClicked($event)" 
    @extend-search="emitExtendSearch(appendSearchParams('org', $event))" />
</template>

<script>
import { genericResultsMixin } from '@/mixins/search';
import { searchJumpMixin } from '@/mixins/search';

export default {
    mixins: [genericResultsMixin, searchJumpMixin],
}
</script>