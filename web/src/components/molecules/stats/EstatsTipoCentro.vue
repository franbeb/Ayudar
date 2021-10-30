<template>
  <div class="box">
       <StatHeader title="Cantidad de Tipo de Centros"
      desc="Dado un tipo de centro, muestra la cantidad de tipo de centros cargados en el sistema" />
    <br>
    <div >
      <span class="align-middle">
          <ve-funnel  :settings="chartSettings" :display-percentage="true" :data="chartData"></ve-funnel>
        </span>
    </div>
      

  </div>
</template>



<script>
import axios from "axios";
import veFunnel from "v-charts/lib/funnel.common";
import StatHeader from "../../atoms/stats/StatHeader"

export default {
  name: "EstatsTipoCentro",
  components: { veFunnel, StatHeader },
  data() {
    return {
      respuesta: null,
      rows_data: {},
      chartSettings : {
        ascending: false,

      },
      chartData: {
        columns: ["status", "value"],
        rows: [],
      },
    };
  },
  mounted() {
    this.call_api();
  },
  methods: {
    call_api() {
      axios
        .get("https://admin-grupo2.proyecto2020.linti.unlp.edu.ar/api/estadisticas-tipo-centro")
        .then((response) => this.obtain_rows(response["data"]));
    },

    obtain_rows(lista) {
      this.rows = [];

      for (var key in lista) {
        this.rows.push({ status: key, value: lista[key] });
      }
      console.log(this.rows);
      this.chartData.rows = this.rows;
    },
  },
};
</script>



