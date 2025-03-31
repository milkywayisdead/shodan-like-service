<template>
<h3>{{ locale.search.details }}</h3>
<bar-chart :chart-data="chartData" />
</template>

<script>
import { detailsMixin } from '@/mixins/search'

export default {
    mixins: [detailsMixin],
}
</script>