<template>
  <div class="mb-10">
    <!-- como recorrer un diccionario con diccionarios? pues con dos for, al lobby -->

    <div >
        <span v-for="(item, index) in respuesta" v-bind:key="index">
          <div v-if="index > 0">
            <p style="color: red" v-html="item['msg']"></p>
          </div>


        </span>
    </div>
    <div v-if="status==201"  >
      <p style="color:green">Carga de turno exitosa</p>
      {{resetForm()}}
    </div>

    <div>
      <form v-on:submit.prevent="submitForm">
        <div class="form-group">
          <label for="name">Nombre</label>
          <input
            type="text"
            class="form-control"
            id="name"
            placeholder="Ingrese nombre"
            v-model="form.name"
            required
          />
        </div>
        <div class="form-group">
          <label for="surname">Apellido</label>
          <input
            type="text"
            class="form-control"
            id="surname"
            placeholder="Ingrese apellido"
            v-model="form.surname"
            required
          />
        </div>
        <div class="form-group">
          <label for="email">Email</label>
          <input
            type="email"
            class="form-control"
            id="email"
            placeholder="name@example.com"
            v-model="form.email"
            required
          />
        </div>
        <div class="form-group">
          <label for="phone">Telefono</label>
          <input
            type="phone"
            class="form-control"
            id="phone"
            placeholder="(Código_De_Área - Num) 221-677350"
            v-model="form.phone"
            required
          />
        </div>
        <div>
          <label for="example-datepicker">Seleccione una fecha</label>
          <datepicker
            :bootstrap-styling="true"
            input-class="form-control"
            id="datepicker"
            v-model="fecha"
            required
            :openDate="openDate"
            :disabled-dates="{ to:date }"
            @closed="borrarHorario()"
          >
          </datepicker>
        </div>

        <div class="form-group">
          <label for="refer">Horarios de turnos disponibles</label>
          <select
            name="refer"
            class="form-control"
            id="refre"
            @mouseover="dateSelected()"
            v-model="form.horario"
         

            required
          >
            <option selected="true">Seleccione horario</option>
            <option
              v-for="(item, index) in $globalData.horarios"
              v-bind:key="index"
            >
              {{ item }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <button class="button">Crear turno</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Datepicker from "vuejs-datepicker";
import moment from "moment";
import Vue from "vue";
Vue.prototype.$globalData = Vue.observable({
  horarios: null,
  fecha: new Date(),
});

export default {
  name: "SolicitarTurno",
  components: {
    Datepicker,
  },

  props: [ 'id' ],
  // para recibir por fuera de la ruta (desde el otro componente se pasa como :nombre="valor")

  data() {
    return {
      form: {
        name: "",
        surname: "",
        email: "",
        horario: "",
        fecha: "",
      },
      openDate: null,
      reactive: true,
      date: null,
      respuesta: null,
      status: null,
      errores: null,
      fecha:null,
      borrarHorario() {
        this.$globalData.horarios = null;
        this.form.horario='';
        ///this.$forceUpdate();
      },

      dateSelected() {
        let valorFecha = document.getElementById("datepicker").value;
        this.obtenerHorarios(valorFecha);
      },

      obtenerHorarios(valorFecha) {
        let fecha = moment(String(valorFecha)).format("YYYY-MM-DD");
        axios
          .get(
            "https://admin-grupo2.proyecto2020.linti.unlp.edu.ar/turns/" +
              String(fecha) +
              "/free_hours/" +
              this.id
          )
          .then((response) => (this.$globalData.horarios = response["data"]));
      },
      submitForm() {
        this.form.fecha = document.getElementById("datepicker").value;
        let fecha = moment(String(this.form.fecha)).format("DD/MM/YYYY");
        this.respuesta = null;
        axios
          .post(
            "https://admin-grupo2.proyecto2020.linti.unlp.edu.ar/centros/" +
              this.id +
              "/reserva?email=" +
              this.form.email +
              "&fecha=" +
              fecha +
              "&starting_time=" +
              this.form.horario +
              "&tel_donante=" +
              this.form.phone +
              "&name=" +
              this.form.name+
              "&surname="  +
              this.form.surname
          )
          .then((response) => (this.respuesta = response['data'], this.status = response['status']
          ));


      },
      resetForm(){
          this.form.horario='';
          this.form.phone='';
          this.form.name='';
          this.form.surname='';
          this.form.email='';
          this.form.fecha='';
          this.status=null;
          this.fecha= new Date();
          alert('Turno creado con exito');

      },
      fechaActual(){

        return this.date
      }

    };
  },
  method: {},

  mounted() {
    // alert(this.id)
    //this.form.fecha = String(new Date());
    this.fecha=new Date()
    this.openDate= new Date()
    this.date= new Date()
    this.date.setDate( this.date.getDate() - 1)

    this.obtenerHorarios(new Date());
  },
};
</script>


<style>
label{
  color:black
}
span{
  color:black
}
</style>
