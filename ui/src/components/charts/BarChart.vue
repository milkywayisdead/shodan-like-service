<template>
<div :id="containerId">
    <apexchart
      type="bar"
      :options="chartOptions"
      :series="limitedSeries"
      :height="height"
    ></apexchart>
</div>
</template>

<script>
import VueApexCharts from "vue3-apexcharts";
import { DETAILS_MAX_ITEMS } from '@/utils/constants'

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

        let cats = this.categories
        if(cats.length > DETAILS_MAX_ITEMS){
            cats = cats.slice(0, DETAILS_MAX_ITEMS)
        }

        let series = this.series
        if(this.categories.length > DETAILS_MAX_ITEMS){
            series = [{data: series[0].data.slice(0, DETAILS_MAX_ITEMS)}]
        }

        return {
            containerId: `c${+new Date()}`,
            showChart: false,
            height: cats.length*80,
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
                    categories: cats,
                },
            },
            limitedSeries: series, 
        }
    },
}
</script>