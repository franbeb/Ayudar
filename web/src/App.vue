<template>
  <div id="app">
    <div id="nav">
      <a href="https://admin-grupo2.proyecto2020.linti.unlp.edu.ar/">Admins</a>
    </div>
    <router-view/>

  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color:rgba(0,0,0,0);
}

#nav {
  display: flex;
  justify-content: center;
  position: fixed;
  background: white;
  width: 100%;
  top: 0%;
  left: 0%;
}

#nav a {
  margin: 1rem 0.5rem;
  text-decoration: none;
  color: #00ADC1;
}
</style>
