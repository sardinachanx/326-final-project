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
    },
    rememberMe: localStorage.getItem('rememberMe') || false,
    error: null
  },
  mutations: {
    setToken (state, { access, refresh, rememberMe }) {
      if (rememberMe) {
        localStorage.setItem('rememberMe', true)
        state.rememberMe = true
      } else {
        localStorage.removeItem('rememberMe')
        state.rememberMe = false
      }

      state.access = access
      state.refresh = refresh
      if (state.rememberMe) {
        localStorage.setItem('access', access)
        localStorage.setItem('refresh', refresh)
      } else {
        sessionStorage.setItem('access', access)
        sessionStorage.setItem('refresh', refresh)
      }
    },
    updateToken (state, { access }) {
      state.access = access
      if (state.rememberMe) {
        localStorage.setItem('access', access)
      } else {
        sessionStorage.setItem('access', access)
      }
    },
    removeToken (state) {
      state.access = null
      state.refresh = null
      if (state.rememberMe) {
        localStorage.removeItem('access')
        localStorage.removeItem('refresh')
        localStorage.removeItem('rememberMe')
      } else {
        sessionStorage.removeItem('access')
        sessionStorage.removeItem('refresh')
        sessionStorage.removeItem('rememberMe')
      }
      state.rememberMe = null
    },
    setError (state, error) {
      state.error = error
    }
  },
  actions: {
    obtainToken (state, { email, password, rememberMe }) {
      const payload = {
        email: email,
        password: password
      }

      return axios.post(this.state.endpoints.obtainJWT, payload)
        .then((response) => {
          response.data.rememberMe = rememberMe
          this.commit('setToken', response.data)
        })
        .catch((error) => {
          console.log(error)
        })
    },
    showError (state, error) {
      this.commit('setError', error)
    },
    refreshToken () {
      const payload = {
        refresh: this.state.refresh
      }

      return axios.post(this.state.endpoints.refreshJWT, payload)
        .then((response) => {
          this.commit('updateToken', response.data)
        })
        .catch((error) => {
          console.log(error)
        })
    },
    inspectToken () {
      const accessToken = this.state.access
      const refreshToken = this.state.refresh
      if (accessToken && refreshToken) {
        const decodedAccess = jwtDecode(accessToken)
        const decodedRefresh = jwtDecode(refreshToken)
        const accessExp = decodedAccess.exp
        const refreshExp = decodedRefresh.exp

        if (refreshExp - (Date.now() / 1000) < 0) {
          // TODO: PROMPT USER TO RE-LOGIN, THIS ELSE CLAUSE COVERS THE CONDITION WHERE A TOKEN IS EXPIRED AS WELL
          return Promise.reject(new Error('need to re-login'))
        }

        if (accessExp - (Date.now() / 1000) < 1800) {
          return this.dispatch('refreshToken')
        } else {
          // can continue to use the current token
          return Promise.resolve()
        }
      } else {
        // need to log in
        return Promise.resolve()
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
