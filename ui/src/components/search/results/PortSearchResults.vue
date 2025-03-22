<template>
    <search-results-block 
        :hosts="info.hosts || []" 
        :tops="(info.tops || [])[0] || {}"
        :totals="totals" />
    </template>

<script>
export default {
    props: {
        info: {
            type: Object,
            default: {}
        }
    },
    computed: {
        totals(){
            const ports = (this.info.ports || [])[0]
            return {
                hosts: this.info.hosts_total,
                ports: ports?.total_ports_count
            }
        }
    }
}
</script>