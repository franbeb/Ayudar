<template>
  <div>
    <StatHeader title="Horarios mas reservados historicamente"
    desc="Cantidad historica de turnos reservados segun el dia de la semana y la hora." />

    <ve-heatmap :data="chartData" height="1000px" :settings="chartSettings"></ve-heatmap>
  </div>
</template>

<script>
  import veHeatmap from "v-charts/lib/heatmap.common"
  import axios from "axios"
  import StatHeader from "../../atoms/stats/StatHeader"

  export default {
    name: "TurnStat",
    components: { veHeatmap, StatHeader },
    data () {
      this.chartSettings = {
        height: "10000px",
        yAxisList: ["9:00", "9:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30", "15:00", "15:30"],
        xAxisList: ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
      }
      return {
        chartData: {
          columns: ['weekday', 'hour', 'reserved'],
          rows: []
        }
      }
    },
    methods: {
      call_api() {
        axios.get("https://admin-grupo2.proyecto2020.linti.unlp.edu.ar/api/all_turns").then((response) => { this.chartData.rows = response["data"] })
      }
    },
    mounted() {
      this.call_api()
    }
  }
</script>
