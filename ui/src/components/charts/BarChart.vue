<template>
<div :id="containerId">
    <Bar v-if="showChart"
        id="details-bar"
        style="background-color:#212121;"
        :options="chartOptions"
        :data="chartData"
        :height="height" 
        :width="width" />
</div>
</template>

<script>
import { Bar } from 'vue-chartjs';
import { 
    Chart as ChartJS, 
    Title, 
    Tooltip,
    BarElement,
    LinearScale,
    CategoryScale,
} from 'chart.js'
import ChartDataLabels from 'chartjs-plugin-datalabels';

ChartJS.register(Title, BarElement, Tooltip, LinearScale, CategoryScale, ChartDataLabels)


const barThickness = 50

export default {
    components: {Bar},
    props: {
        chartData: {
            type: Object,
            default: {
                labels: [],
                datasets: []
            },
        },
        height: {
            type: Number,
            default: 500
        },
    },
    data(){
        return {
            containerId: `c${+new Date()}`,
            chartOptions: {
                responsive: false,
                indexAxis: 'y',
                barThickness: barThickness,
                scales: {
                    y: {
                        ticks: {
                            display: false
                        }
                    } 
                }
            },
            showChart: false,
            width: 0,
        }
    },
    methods: {
        getWidth(){
            const rect = document.getElementById(this.containerId).getBoundingClientRect()
            return rect.width
        }
    },
    mounted(){
        this.width = this.getWidth()
        this.showChart = true
    }
}
</script>