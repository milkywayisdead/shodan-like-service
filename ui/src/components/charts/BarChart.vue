<template>
<div :id="containerId">
    <apexchart
      type="bar"
      :options="chartOptions"
      :series="series"
      :height="height"
    ></apexchart>
</div>
</template>

<script>
import VueApexCharts from "vue3-apexcharts";

export default {
    components: {
        apexchart: VueApexCharts,
    },
    props: {
        categories: {
            type: Array,
            default: []
        },
        _categories: {
            type: Array,
            default: []
        },
        series: {
            type: Array,
            default: []
        }
    },
    emits: ['category-click'],
    data(){
        const _this = this
        return {
            containerId: `c${+new Date()}`,
            showChart: false,
            height: this.categories.length*80,
            chartOptions: {
                chart: {
                    id: 'details-bar',
                    events: {
                        click(event, chartContext, opts) {
                            const target = event.target
                            const parent = target.parentElement
                            try {
                                if(target.tagName !== 'tspan') return
                                if(parent?.tagName !== 'text') return
                                if(
                                    !parent.classList.contains('apexcharts-text') || 
                                    !parent.classList.contains('apexcharts-yaxis-label')
                                ) return
                            } catch(err){
                                return
                            }

                            let cat = ''
                            for(const child of parent.children){
                                if(child.tagName === 'title'){
                                    cat = child.textContent
                                    break
                                }
                            }

                            if(!_this._categories.includes(cat)) return
                            _this.$emit('category-click', cat)
                        }
                    },
                    toolbar: {
                        show: false
                    }
                },
                grid: {
                    show: false,
                },
                yaxis: {
                    labels: {
                        style: {
                            fontSize: '14px',
                            colors: 'white'
                        },
                    } 
                },
                tooltip: {
                    enabled: false,
                },
                plotOptions: {
                    bar: {
                        horizontal: true,
                    }
                },
                xaxis: {
                    categories: this.categories,
                },
            },
        }
    },
}
</script>