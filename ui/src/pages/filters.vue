<template>
<h1>{{ locale.nav.filters }}</h1>
</template>

<script>
import { storeMixin } from '@/mixins/store';

export default {
    mixins: [storeMixin],
}
</script>

<route lang="yaml">
meta:
    layout: base
</route>