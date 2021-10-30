<template>
  <div>
    <div class="landing">
      <div class="img-container">
        <img class="logo" alt="Ayudar Logo" src="../../assets/logo.svg">
      </div>
      <Options/>
    </div>
    <SiteExplanation/>
  </div>
</template>

<script>
import Options from '../molecules/Options.vue'
import SiteExplanation from '../molecules/SiteExplanation.vue'

export default {
  name: 'Home',
  components: {
    Options,
    SiteExplanation
  }
}
</script>

<style>
.landing {
  width: 100%;
  display: flex;
  justify-content: space-evenly;
  align-items: center;
  margin: 10rem 0rem;
}

.img-container {
  width: 40%;
  height: 18rem;
  display: flex;
  justify-content: center;
}
</style>
