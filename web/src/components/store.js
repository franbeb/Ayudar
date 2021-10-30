import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
  state:{
    empty: false
  },
  mutations:{
    increment(state, payload) {
      state.count += payload.amount
    },
    decrement(state,payload){
      state.count-= payload.amount
    }
  }
})

export default store