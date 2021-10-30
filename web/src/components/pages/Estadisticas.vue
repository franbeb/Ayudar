<template>
    <div>
      <div class="landing">
        <div class="img-container">  <img class="logo" alt="Ayudar Logo" src="../../assets/logo.svg">
        </div> <Options/> </div>
        <div class="container">
          <div> <Estats1/> </div>
          <div> <EstatsTipoCentro/> </div>
          <div> <TurnStat /> </div>
        </div>
    </div>
</template>

<script>
import Options from '../molecules/Options.vue'
import Estats1 from '../molecules/stats/Estats1'
import EstatsTipoCentro from '../molecules/stats/EstatsTipoCentro'
import TurnStat from '../molecules/stats/TurnStat'


export default {
  name: 'Estadisticas',
  components: {
    Options,
    Estats1,
    EstatsTipoCentro,
    TurnStat
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
</style>


