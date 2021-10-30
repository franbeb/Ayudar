<template>
<div>
  <div class = "options"> <Options></Options>  </div>
  <br> <br> <br>
  <div class="container card col-md-6">
    
    <h2>Cargar Centro</h2>
    <div>
      <form v-on:submit.prevent="submit">
        <div class="form-group">
          <label for="email">Email</label>
          <input
            required
            type="email"
            class="form-control"
            id="email"
            placeholder="name@example.com"
            v-model="form.email"
          />
          <div class="form-group">
            <label for="nombre">Nombre</label>
            <input
              type="text"
              class="form-control"
              id="nombre"
              placeholder="Ingrese nombre"
              v-model="form.nombre"
            />
          </div>
        </div>
        <div class="form-group">
          <label for="direccion">Direccion</label>
          <input
            type="text"
            class="form-control"
            id="direccion"
            placeholder="Ingrese direccion"
            v-model="form.direccion"
          />
        </div>
        <div class="form-group">
          <label for="telefono">Telefono</label>
          <input
            type="telefono"
            class="form-control"
            id="telefono"
            placeholder="231414212"
            v-model="form.telefono"
          />
        </div>
        <div class="form-group">
          <label> Hora de apertura: </label>
          <input
            id="hora_cierre"
            name="hora_cierre"
            required=""
            type="time"
            value=""
            v-model="form.hora_apertura"
          />
        </div>
        <div class="form-group">
          <label> Hora de cierre: </label>
          <input
            id="hora_cierre"
            name="hora_cierre"
            required=""
            type="time"
            value=""
            v-model="form.hora_cierre"
          />
  
        </div>
        <div class="form-group">
          <label for="web">Web</label>
          <input
            type="web"
            class="form-control"
            id="web"
            placeholder="www.example.com"
            v-model="form.web"
          />
        </div>
        <div class="form-group">
          <label> Protocolo vista: </label>
          <input
            type="file"
            name="file"
            accept="application/pdf"
            v-on:change="fileChange()"
            id="file"
            ref="file"
          />
        </div>

        <!-- <div class="form-group">
          <label for="tipo_centro">Tipo</label>
          <select
            name="refer"
            class="form-control"
            id="refre"
            v-model="form.tipo_centro"
            @mouseenter="dateSelected()"
          >
        
            <option value=16>Alimentos </option>
            <option value=17>Plasma</option>
            <option value=18>Ropa </option>
          </select>
        </div> -->

        <div class="form-group">
          <select
            required=""
            name="tipos_centros"
            class="form-control"
            multiple=""
            v-model="form.tipo_centro"
          >
            <option selected="true" value="16">Alimentos</option>

            <option value="17">Plasma</option>

            <option value="18">Ropa</option>
          </select>
        </div>
        <div class="form-group">
          <l-map
            style="height: 350px"
            :zoom="zoom"
            :center="center"
            v-on:click="addMarker"
          >
            <l-tile-layer :url="url"> </l-tile-layer>
            <l-marker
              v-for="(m, i) in markers"
              v-bind:key="i"
              :lat-lng="m"
              @click="removeMarker(i)"
              ><p>m</p></l-marker
            >
          </l-map>
        </div>
        <div class="form-group"></div>

        <div class="form-group">
          <label for="municipio">Municipio</label>
          <select
            required
            name="refer"
            class="form-control"
            id="refre"
            v-model="form.municipio"
          >
            <option v-for="m in municipios" v-bind:key="m.id" :value="m.id">
              {{ m.name }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <vue-recaptcha
            @verify="submitForm()"
            @expired="onExpired"
            :sitekey="sitekey"
          >
            <button id="idCaptcha" hidden>...</button>

          </vue-recaptcha>
            <button class="button">Crear centro</button>

        </div>
      </form>
    </div>
  </div>
</div>

</template>

<script>
import axios from "axios";
import L from "leaflet";
import { LMap, LTileLayer, LMarker } from "vue2-leaflet";
import VueRecaptcha from "vue-recaptcha";
import Options from '../molecules/Options'

export default {
  name: "Centro",
  components: {
    Options,
    LMap,
    LTileLayer,
    LMarker,
    VueRecaptcha,
  },
  data() {
    return {
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      markers: [L.latLng(Math.random(),Math.random())],
      zoom: 6,
      center: [-36.264646899345905, -60.22970892840804],
      municipios: axios
        .get(
          "https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios?per_page=150"
        )
        .then((Response) => {
          this.municipios = Response.data.data.Town;
        }),
      form: {
        nombre: "",
        direccion: "",
        telefono: "",
        hora_apertura: "",
        hora_cierre: "",
        web: "",
        tipo_centro: [],
        municipio: "",
        surname: "",
        email: "",
        horario: "",
        fecha: "",
        longitud: "",
        latitud: "",
        protocolo_vista: "",
      },
      sitekey: "6LemSAQaAAAAAJ6Yn8HYDqA3-DCCw3JHd7w5i336",
      statusCaptcha: false,
      pdf: "",
      file:null,
      // RECAPTCHA_PUBLIC_KEY:'"6LdBKwQaAAAAAPkG9bO79tr3cT7cgR_WS_d7M-IT"',
      // process.env.API_URL: '"http://localhost:55348/api'"
      submit(){

          document.getElementById("idCaptcha").click();

      },
      submitForm() {
        console.log("mandado");
        console.log(this.form.tipo_centro);
        ///   if (this.statusCaptcha){
        if (this.markers) {
          this.form.latitud = this.markers[0]["lat"];
          this.form.longitud = this.markers[0]["lng"];
        }
        let formData = new FormData();
        formData.append('file', this.file);
        formData.append('nombre', this.form.nombre);
        formData.append('direccion', this.form.direccion);
        formData.append('telefono', this.form.telefono);
        formData.append('hora_apertura', this.form.hora_apertura);
        formData.append('hora_cierre', this.form.hora_cierre);
        formData.append('tipo_centro', this.form.tipo_centro);
        formData.append('municipio', this.form.municipio);
        formData.append('web', this.form.web);
        formData.append('email', this.form.email);
        formData.append('latitud', this.form.latitud);
        formData.append('longitud', this.form.longitud);

        axios
          .post(
            "https://admin-grupo2.proyecto2020.linti.unlp.edu.ar/centros",
            formData,
             {
              headers: {
                "Content-Type": "multipart/form-data",
              },
            }
          ).then(this.resetForm());
         /// this.submitFormPdf();
      },
     
      resetForm() {
        this.form.nombre = "";
        this.form.direccion = "";
        this.form.hora_apertura = "";
        this.form.hora_cierre = "";
        this.form.web = "";
        this.form.tipo_centro = [];
        this.form.municipio = "";
        this.form.email = "";
        this.form.longitud = "";
        this.form.latitud = "";
        this.markers = [L.latLng(Math.random(),Math.random())]
        //        this.form.protocolo_vista = "";
        this.form.telefono = "";

        alert("Centro creado con exito");
      },
      onVerify(response) {
        console.log("Verify ", response);
        
        //this.statusCaptcha = true
      },
      onExpired() {
        alert("Captcha expired");
        ////this.statusCaptcha = false
      },
    };
  },
  methods: {
    fileChange() {
      this.file = this.$refs.file.files[0];

    },

    removeMarker(index) {
      //   this.markers.splice(index, 1);
      console.log(index);
    },
    addMarker(event) {
      this.markers.pop();
      this.markers.push(event.latlng);
    },
  },
};
</script>

<style>
label {
  color: black;
}
span {
  color: black;
}
h2 {
  color: black;
}
input {
  color: black;
}
.options{
  margin-top:50px;
}
</style>