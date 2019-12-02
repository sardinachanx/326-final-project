<template>
  <div>
    <div id="app">
      <header>
        <p style="display: inline; margin: 0">Databaes</p>
        <nav>
          <div class="mainnav" v-if="loggedIn">
            <router-link to="/">Home</router-link> |
            <router-link to="/homeworkplanner">Homework Planner</router-link> |
            <router-link to="/classes">Classes</router-link> |
            <router-link to="/search">Search</router-link> |
            <router-link to="/profile">Profile</router-link>
          </div>
          <div class="loginnav">
            <router-link to="/login" v-if="!loggedIn">Login</router-link>
            <a href="" v-on:click.stop.prevent="logout" v-if="loggedIn">Logout</a>
          </div>
        </nav>
      </header>
      <router-view id="body" :classes="loggedIn ? currentUser.classes : null" :user="currentUser"/>
      <div id="toast" v-if="errorLoading != null || !$auth.ready()">
        Oops! Something went wrong.
        <br />
        <div v-if="errorLoading != null">&#x26a0; {{ errorLoading }}</div>
        <div v-if="errorLoading == null">&#x26a0; Couldn't connect <br /> to the server </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as api from '@/api.js'

export default {
  name: 'app',
  data: function () {
    return {
      currentUserId: 0,
      currentUser: null,
      errorLoading: null
    }
  },
  computed: {
    loggedIn: function () {
      return this.currentUser !== null
    }
  },
  methods: {
    showError: function (error) {
      this.errorLoading = error
    },
    logout: function () {
      // TODO: actually logout
      this.currentUser = null
    }
  },
  mounted: function () {
    // TODO: load data from backend

    /* this.currentUser = {
      email: 'test@test.com',
      username: 'blah',
      classes: [{
        name: 'Blah',
        id: 0,
        assignments: [
          {
            name: 'Assignment one',
            totalTime: 2,
            averageTime: 1,
            id: 0
          }
        ]
      }]
    } */

    api.getStudent(this.currentUserId).then((student) => {
      this.currentUser = student
      // return api.getCourses()
    }).catch(this.showError)
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
  background: #FF0000FF;
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
  background-color: #f5f5f5;
  width: stretch;
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
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
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
}
</style>
