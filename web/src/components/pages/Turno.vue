<template>
    <div>
        <div class="landing">
        <div class="img-container">
            <img class="logo" alt="Ayudar Logo" src="../../assets/logo.svg">
        </div>
            <Options/>
        </div>
        <div class="solicitar-turno">
            <SolicitarTurno/>
        </div>
    </div>
</template>

<script> // for what
import Options from '../molecules/Options.vue'
import SolicitarTurno from '../molecules/SolicitarTurno.vue'

export default {
  name: 'Turno',
  components: {
    Options,
    SolicitarTurno,
  }
}
</script>

<style>
.landing {
  width: 100%;
  display: flex;
  justify-content: space-evenly;
  align-items: center;
}

.img-container {
  width: 40%;
}

.solicitar-turno{
  padding:13%;
}
</style>


