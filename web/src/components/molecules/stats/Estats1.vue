<template>

  <div class="box">
    <StatHeader title="Cantidad de turnos asignados por Centro"
      desc="Dada una fecha específica, muestra la cantidad de turnos asignados por cada centro habilitado" />
    <br>
    <div class="fecha-select" >
      <label for="example-datepicker">Seleccione una fecha para calcular</label>
      <datepicker
        :bootstrap-styling="true"
        input-class="form-control"
        :open-date="openDate"
        @selected="dateSelected()"
        id="fecha_turnos_x_centro"
        v-model="fecha"
        required
      >
      </datepicker>
    </div>
    <br>
    <ve-ring :data="chartData" :settings="chartSettings"></ve-ring>
  </div>
</template>


<script>
import axios from "axios";
import Datepicker from "vuejs-datepicker";
import moment from "moment";
import veRing from "v-charts/lib/ring.common";
import StatHeader from "../../atoms/stats/StatHeader"


export default {
  components: { Datepicker, veRing, StatHeader }, // VGeosearch
  data() {
    this.chartSettings = {
        roseType: "radius",

    };
    return {
        openDate: new Date(),
        fecha: new Date(),
        rows_data:{},
        chartData: {
            columns: ["nombre", "asignados", "total"],
            rows: [],
        },
    };
  },
  mounted() {
    this.call_api(new Date());
  },
  methods: {
    dateSelected() {
        let fecha = document.getElementById("fecha_turnos_x_centro").value;
        this.call_api(fecha);
    },

    call_api(fecha) {
        axios
            .get("https://admin-grupo2.proyecto2020.linti.unlp.edu.ar/centros_statistics/" + moment(String(fecha)).format("YYYY-MM-DD"))
            .then((c) => this.centros_rows(c.data.centros) );
    },

    centros_rows(centros) {
        console.log(centros)
        this.rows=[];
        centros.map(c =>{
            this.rows.push({
                nombre: c.nombre,
                asignados: c.asignados,
                total: c.total,
              })
        })
        if (this.rows != [] ){
            this.chartData.rows = this.rows;
        }
        else{
            alert('No se encontraron turnos asignados en ningún centro para el día seleccionado')
        }
    },
  },
};
</script>


<style>
.fecha-select{
    position: relative;
    display: flex;
    flex-flow: column wrap;
    align-items: center;
}
</style>
