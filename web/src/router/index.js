import Vue from 'vue'
import VueRouter from 'vue-router'
import Turno from '../components/pages/Turno.vue'
import Home from '../components/pages/Home.vue'
import Centro from '../components/pages/Centro.vue'
import Centros from '../components/pages/Centros.vue'
import Estadisticas from '../components/pages/Estadisticas.vue'


Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/turno/:id',
    name: 'Turno',
    component: Turno
  },
  {
    path: '/Centro',
    name: 'Centro',
    component: Centro
  },
  {
    path: '/mapa-centros',
    name: 'Mapa de Centros',
    component: Centros
  },
  {
    path: '/estadisticas',
    name: 'Estadisticas',
    component: Estadisticas
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
