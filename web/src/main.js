import '@babel/polyfill'
import 'mutationobserver-shim'
import Vue from 'vue'
import './plugins/bootstrap-vue'
import './plugins/axios'
import App from './App.vue'
import router from './router'
import VModal from "vue-js-modal"


import { LMap, LTileLayer,LMarker,LPopup,LIcon , LTooltip } from 'vue2-leaflet'
import { Icon } from 'leaflet';

// Font awesome configuration
import { library } from '@fortawesome/fontawesome-svg-core'
import { faChartBar, faClinicMedical, faMapMarkedAlt } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faChartBar, faClinicMedical, faMapMarkedAlt)
Vue.component('font-awesome-icon', FontAwesomeIcon)

Vue.use(VModal);

Vue.component('l-map', LMap);
Vue.component('l-tile-layer', LTileLayer);
Vue.component('l-marker', LMarker);
Vue.component('l-popup', LPopup);
Vue.component('l-icon',LIcon);
Vue.component('l-tooltip',LTooltip);
delete Icon.Default.prototype._getIconUrl;
Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

new Vue({
  render: h => h(App),
  components: { App },
  router,
  template: '<App/>',
}).$mount('#app');
