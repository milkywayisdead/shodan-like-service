<template>
<h3>Подробности</h3>
<Bar
    id="ports-details-bar"
    style="background-color:#212121;max-height:400px"
    :options="chartOptions"
    :data="chartData" />
</template>

<script>
import { storeMixin } from '@/mixins/store';
import { Bar } from 'vue-chartjs';
import { 
    Chart as ChartJS, 
    Title, 
    Tooltip, 
    //Legend, 
    BarElement,
    LinearScale,
    CategoryScale,
} from 'chart.js'
import ChartDataLabels from 'chartjs-plugin-datalabels';

ChartJS.register(Title, BarElement, Tooltip, LinearScale, CategoryScale, ChartDataLabels)

export default {
    mixins: [storeMixin],
    components: {Bar},
    data(){
        return {
            _chartData: {
                labels: [],
                datasets: []
            },
            chartOptions: {
                responsive: true,
            },
            showChart: false,
        }
    },
    methods: {
        setDetails(){
            const data = this.store.details
            const labels = data.map(item => item._id)
            const datasets = [{data: data.map(item => item.count), backgroundColor: '#36a2eb'}]
            this._chartData = {
                labels: labels,
                datasets: datasets,
            }
        },
    },
    computed: {
        chartData(){
            return this._chartData
        }
    }
}
</script>