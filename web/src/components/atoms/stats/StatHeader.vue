
<template>
  <div>
    <div id="titulo"><h2>{{title}}</h2></div>
    <div class="hidden">{{desc}}</div>
  </div>
</template>

<script>
export default {
  name: 'StatHeader',
  props: {
    title: String,
    desc: String
  }
}
</script>

<style scoped>
div.hidden { display:none; }

#titulo {
 transition: all 2s ease;
}

#titulo:hover + div.hidden {
  display:block;
  background-color: rgba(0, 0, 0, 0.039);
  border-radius: 13px;
  color: rgba(0, 0, 0, 0.454);

  width: fit-content;
  margin:auto;
  padding: 0 .7rem;

}
</style>
