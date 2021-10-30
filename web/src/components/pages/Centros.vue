<template>
    <div>
        <div class="landing">
        <div class="img-container">
            <img class="logo" alt="Ayudar Logo" src="../../assets/logo.svg">
        </div>
            <Options/>
        </div>
        <div>
            <CentrosMap/>
        </div>
    </div>
</template>

<script> // for what
import Options from '../molecules/Options.vue'
import CentrosMap from '../molecules/CentrosMap.vue'

export default {
  name: 'Centros',
  components: {
    Options,
    CentrosMap,
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


