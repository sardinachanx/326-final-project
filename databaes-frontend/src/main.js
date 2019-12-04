import Vue from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import VueAxios from 'vue-axios'
import jwtDecode from 'jwt-decode'
import Vuex from 'vuex'

Vue.use(Vuex)
Vue.use(VueAxios, axios)
Vue.axios.defaults.baseURL = 'http://localhost:8000/api/'

const store = new Vuex.Store({
  state: {
    refresh: localStorage.getItem('refresh'),
    access: localStorage.getItem('access'),
    endpoints: {
      obtainJWT: 'login/',
      refreshJWT: 'refresh/'
    }
  },
  mutations: {
    updateToken (state, { access, refresh }) {
      state.access = access
      state.refresh = refresh
      localStorage.setItem('access', access)
      localStorage.setItem('refresh', refresh)
    },
    removeToken (state) {
      localStorage.removeItem('t')
      state.jwt = null
    }
  },
  actions: {
    obtainToken (state, { email, password }) {
      const payload = {
        email: email,
        password: password
      }

      axios.post(this.state.endpoints.obtainJWT, payload)
        .then((response) => {
          this.commit('updateToken', response.data)
        })
        .catch((error) => {
          console.log(error)
        })
    },
    refreshToken () {
      const payload = {
        token: this.state.refresh
      }

      axios.post(this.state.endpoints.refreshJWT, payload)
        .then((response) => {
          this.commit('updateToken', response.data.token)
        })
        .catch((error) => {
          console.log(error)
        })
    },
    inspectToken () {
      const token = this.state.refresh
      if (token) {
        const decoded = jwtDecode(token)
        const exp = decoded.exp
        const origIat = decoded.orig_iat

        if (exp - (Date.now() / 1000) < 1800 && (Date.now() / 1000) - origIat < 628200) {
          this.dispatch('refreshToken')
        } else if (exp - (Date.now() / 1000) < 1800) {
          // DO NOTHING, DO NOT REFRESH
        } else {
          // TODO: PROMPT USER TO RE-LOGIN, THIS ELSE CLAUSE COVERS THE CONDITION WHERE A TOKEN IS EXPIRED AS WELL
        }
      }
    }
  }
})

store.blah = 'blah'

Vue.router = router

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
