<template>
<div style= "height:100vh">
    <l-map
        style="height:90%; width:100%"
        :zoom="zoom"
        :center="center">

        <l-tile-layer :url="url"></l-tile-layer>
        <!--<v-geosearch :options="geosearchOptions" ></v-geosearch>-->
        <l-marker v-for="(cent, index) in centros" :key="index" :lat-lng="odd_format(cent.latlng[0],cent.latlng[1])">
            <l-popup>
                <h1> {{cent.nombre}} </h1>

                <hr style="height:2px;border-width:0;color:gray;background-color:gray">
                <h5> DIRECCION: {{cent.direccions}} </h5>
                <h5> HORARIO: {{ cent.hora_apertura}} - {{cent.hora_cierre}}</h5>

                <hr style="height:1px;border-width:0;color:gray;background-color:gray">
                <span class="hiperlinks">
                    <a class="email" v-bind:href="'mailto:' + cent.email">{{cent.email}} </a>
                    //
                    <a class="web" :href="'https://' + cent.web"> {{cent.web}} </a>
                </span>

                <hr style="height:1px;border-width:0;color:gray;background-color:gray">
                <h6> TIPO DE DONACIONES:</h6>
                <h6 v-for="(donacion, index) in cent.tipo" :key="index"> {{donacion}} </h6>
                <br>
                <button class="button" @click="showModal(cent.id, cent.nombre, $event)"> SOLICITAR UN TURNO </button>

            </l-popup>
        </l-marker>

    </l-map>

    <modal name="crear-turno" class="crear-turno">
        <h1>
            {{nombre_centro_turno}}
            <span>
                <button class="button-cerrar" @click="closeModal"> x </button>
            </span>
        </h1>
        <SolicitarTurno :id="id_centro_turno"></SolicitarTurno>
    </modal>

</div>
</template>

<script>
import axios from 'axios'
import 'leaflet/dist/leaflet.css';
import { OpenStreetMapProvider } from 'leaflet-geosearch';
import SolicitarTurno from '../molecules/SolicitarTurno'
// import VGeosearch from 'vue2-leaflet-geosearch';
import L from 'leaflet'

export default {
    components: { SolicitarTurno },// VGeosearch
    data(){
        return {
            url:'https://api.mapbox.com/styles/v1/mapbox/outdoors-v11/tiles/{z}/{x}/{y}?access_token=pk.eyJ1Ijoic2dhcmJpZG9ubmEiLCJhIjoiY2tpajlmcnU1MDBodTJxbXoyd2Q1azA2byJ9.D1E2hTMWuoAPSv22sCPkRg',
            zoom:11,
            center:[-34.9187,-57.956],
            centros:null,
            geosearchOptions: { provider: new OpenStreetMapProvider() },

            id_centro_turno:null,
            nombre_centro_turno:null,

        }
    },

    mounted(){
        axios.get('https://admin-grupo2.proyecto2020.linti.unlp.edu.ar/centros')
        .then((c) => {
            this.centros = c.data.centros;
            this.center = [this.centros[0].lng, this.centros[0].lat];
            console.log(this.markers);
        })
        .catch(error => {
            console.log(error)
            alert(error)
        });

    },
    methods:{
        showModal(id,nombre) {
            this.id_centro_turno = id
            this.nombre_centro_turno=nombre
            this.$modal.show('crear-turno')
        },
        closeModal(){
            this.$modal.toggle('crear-turno')
        },
        odd_format(lat,lng){
            return L.latLng(lat,lng)
        }
    },



};
</script>

<style>
.button {
    appearance: none;
    outline: none;
    border: none;
    cursor: pointer;
    display: inline-block;
    padding: 15px 25px;
    background-image: linear-gradient(to right, rgba(0, 174, 193, 0.461), rgba(139, 139, 139, 0.536));
    border-radius:8px;
    color:#FFF;
    font-size:17px;
    box-shadow: 3px 3px rgb(0,0,0,0.2);
    transition: .4s ease-out;
}

.button:hover{
    font-size: 19px;
    box-shadow: 6px 6px rgba(0,0,0,0.1);
}

.button-cerrar {
    outline: none;
    border: none;
    cursor: pointer;
    padding: 8px 16px;
    background-image: linear-gradient(to right, rgba(193, 0, 0, 0.461), rgba(139, 139, 139, 0.536));
    border-radius:18px;
    color:#FFF;
    font-size:17px;
    box-shadow: 2px 2px rgb(0,0,0,0.2);
    transition: .4s ease-out;
    float: right;

}

.button-cerrar:hover{
    font-size: 22px;
    box-shadow: 6px 6px rgba(0,0,0,0.1);
}
.leaflet-popup-content{
    width: 333px !important;
}
.hiperlinks{
    color:white;
}
.email{
    float: left;
}
.web{
    float: right;
}

#errores {
    color:red;
    background-attachment: fixed;
}

h1 {
    color: #333;
}

.leaflet-popup-content-wrapper{
    text-align: center !important;
}

.vm--modal{
    border-radius: 18px !important;
    height: max-content !important;
    padding: 2% !important;
    max-height: 96vh !important;
    overflow-y: scroll !important;
    top: 2vh !important;
}


</style>
