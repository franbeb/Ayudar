<template>
  <div>
    <Option logo="map-marked-alt" title="Buscá tu centro más cercano" desc="Ver centros de ayuda social en el mapa. También podrás pedir un turno en el centro seleccionado" link="mapa-centros"/>
    <Option logo="clinic-medical" title="Subir centro" desc="Crear una solicitud de carga de un nuevo centro de ayuda social." link="centro"/>
    <Option logo="chart-bar" title="Ver estadisticas" desc="Sección de estadísticas en base a información de los centros de ayuda social." link="/estadisticas" />
  </div>
</template>

<script>
import Option from './../atoms/Option.vue'
export default {
  components: { Option },
  name: 'Options'
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
div {
  width: 60%;
}
</style>
