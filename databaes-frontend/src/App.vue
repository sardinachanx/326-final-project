<template>
  <div>
    <div id="app" v-if="doneLoading">
      <header>
        <a style="display: inline; margin: 0; color: #f5f5f5" href="/">Databaes</a>
        <nav>
          <div class="mainnav" v-if="loggedIn">
            <router-link to="/">Home</router-link> |
            <router-link to="/courses">My Courses</router-link> |
            <router-link to="/compare">Compare</router-link> |
            <router-link to="/profile">Profile</router-link>
          </div>
          <div class="mainnav" v-if="!loggedIn">
            <router-link to="/">Home</router-link> |
            <router-link to="/compare">Compare</router-link>
          </div>
          <div class="loginnav">
            <div v-if="!loggedIn" style="display: inline">
              <router-link to="/login">Login</router-link> |
              <router-link to="/register">Register</router-link>
            </div>
            <a href="" v-on:click.stop.prevent="logout" v-if="loggedIn">Logout</a>
          </div>
        </nav>
      </header>
      <router-view id="body" :user="user" :courses="courses" :specificCourses="specificCourses" v-on:pull-data="pullData"/>
    </div>
    <div id="app" v-if="!doneLoading">
      <h1> Loading... </h1>
    </div>
    <div id="toast" v-if="$store.state.error != null">
      Oops! Something went wrong.
      <br />
      <div v-if="$store.state.error != null">&#x26a0; {{ $store.state.error }}</div>
      <div v-if="$store.state.error == null">&#x26a0; Couldn't connect <br /> to the server </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'app',
  data: function () {
    return {
      user: null,
      doneLoading: false,
      courses: null,
      specificCourses: null
    }
  },
  computed: {
    loggedIn: function () {
      return this.$store.state.access !== null
    },
    config: function () {
      return {
        headers: { 'Authorization': 'Bearer ' + this.$store.state.access }
      }
    }
  },
  methods: {
    logout: function () {
      this.$store.commit('removeToken')
      this.user = null
      this.$router.push('/')
    },
    pullData: function (callback) {
      if (this.loggedIn) {
        let user = axios.get('v1/users/me/', this.config)
        let specificCourses = user.then((response) => {
          return response.data.courses.map((course) => {
            return axios.get('v1/courses/' + course.course + '/', this.config)
          })
        })
        let courses = axios.get('v1/courses/', this.config)
        Promise.all([user, courses, specificCourses])
          .then((response) => {
            Promise.all(response[2]).then((responses) => {
              this.$store.dispatch('showError', null)
              this.user = response[0].data
              this.courses = response[1].data
              this.user.courses = responses.map((response) => {
                return response.data
              })

              this.doneLoading = true
              callback()
            })
          })
          .catch((error) => {
            this.$store.dispatch('showError', error)
            this.doneLoading = true
            callback()
          })
      } else {
        this.doneLoading = true
        callback()
      }
    }
  },
  mounted: function () {
    this.$store.dispatch('inspectToken').then(() => {
      this.pullData(() => {})
    }).catch((error) => {
      this.$store.dispatch('showError', error)
      this.doneLoading = true
    })
  }
}
</script>

<style>
body {
  margin: 0;
}

#toast {
  position: fixed;
  bottom: 20px;
  text-align: center;
  min-height: 60px;
  padding: 30px;
  max-width: 250px;
  min-width: 250px;
  margin-left: -155px;
  border-radius: 3px;
  left: 50%;
  background: #FF0000AA;
  color: white;
  font-size: 1.3em;
}

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: left;
  color: #2c3e50;
}

header {
  padding-left: 15px;
  padding-right: 15px;
  padding-top: 23px;
  padding-bottom: 15px;
  text-align: right;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  background-color: #038288;
  width: stretch;
  font-size: larger;
}

#filler {
  display: block;
  float: none;
  height: 45px;
  background: #F00;
}

nav {
  float: right;
  display: inline-block;
}

.mainnav {
  display: inline;
  margin-right: 20px;
}

.loginnav {
  display: inline;
}

nav a {
  font-weight: bold;
  color: #d3d3d3;
}

nav a.router-link-exact-active {
  color: #f5f5f5;
}

#sidebar {
  width: 250px;
  padding-left: 8px;
  overflow-x: hidden;
  overflow-y: auto;
}

#sidebar {
  position: absolute;
  top: 60px;
  bottom: 0px;
  left: 0px;
}

.body-with-sidebar {
  padding-left: 258px;
}

#body {
  height: stretch;
  margin: auto;
  font-size: larger;
}

/* based on https://purecss.io/buttons/ */
button {
  display: inline-block;
  zoom: 1;
  line-height: normal;
  white-space: nowrap;
  vertical-align: middle;
  text-align: center;
  cursor: pointer;
  -webkit-user-drag: none;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
  -webkit-box-sizing: border-box;
  box-sizing: border-box;
  font-family: inherit;
  font-size: 100%;
  padding: .5em 1em;
  color: #444;
  color: rgba(0,0,0,.8);
  border: 1px solid #999;
  border: none transparent;
  background-color: #e6e6e6;
  text-decoration: none;
  border-radius: 2px;
  margin-left: 10px;
  margin-right: 10px;
}

button:hover {
  background-image: -webkit-gradient(linear,left top,left bottom,from(transparent),color-stop(40%,rgba(0,0,0,.05)),to(rgba(0,0,0,.1)));
  background-image: -webkit-linear-gradient(transparent,rgba(0,0,0,.05) 40%,rgba(0,0,0,.1));
  background-image: linear-gradient(
  transparent,rgba(0,0,0,.05) 40%,rgba(0,0,0,.1));
}

</style>
