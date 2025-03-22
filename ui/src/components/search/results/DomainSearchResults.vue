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