<template>
  <router-link :to="link" class="option">
    <font-awesome-icon :icon="logo" :style="{ width: '20%' }" />
    <div class="text">
      <h3>{{title}}</h3>
      <p>{{desc}}</p>
    </div>
  </router-link>
</template>

<script>
export default {
  name: 'Option',
  props: {
    logo: String,
    title: String,
    desc: String,
    link: String
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.option {
  width: 100%;
  height: max-content;
  padding: 1rem;

  display: flex;
  align-items: center;
  justify-content: flex-end;
  cursor: pointer;

  text-decoration: none;
}

.option:hover {
  border-left: 3.5px solid #00ADC1;
}

.option:hover p {
  display: inline-block;
}

svg {
  font-size: 3rem;
  color: #00ADC1;
  text-align: center;
}

.text {
  text-align: left;
  width: 65%;
  color: #00ADC1;

  display: flex;
  flex-direction: column;
}
h3 {
  font-size: 1.5rem;
  margin: 0;
}

p {
  display: none;
  font-size: 1rem;
  margin: 0;
}
</style>
