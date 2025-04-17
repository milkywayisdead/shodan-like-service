<template>
<Bar
    id="details-bar"
    style="background-color:#212121;"
    :options="chartOptions"
    :data="chartData" />
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
    },
    data(){
        return {
            chartOptions: {
                responsive: true,
                indexAxis: 'y',
            },
            showChart: false,
        }
    },
}
</script>