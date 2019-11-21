<template>
  <div id="app">
    <header>
      <nav>
        <router-link to="/">Home</router-link> |
        <router-link to="/homeworkplanner">Homework Planner</router-link> |
        <router-link to="/classes">Classes</router-link> |
        <router-link to="/search">Search</router-link> |
        <router-link to="/profile">Profile</router-link>
      </nav>
    </header>
    <router-view id="body" :classes="currentUser.classes" :user="currentUser"/>
    <div id="toast" v-if="errorLoading != null">
      Oops! Something went wrong.
      <br />
      &#x26a0; {{ errorLoading }}
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
      currentUser: {},
      errorLoading: null
    }
  },
  methods: {
    showError: function (error) {
      this.errorLoading = error
    }
  },
  mounted: function () {
    // TODO: load data from backend

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
  text-align: left;
  display: flex;
  flex-direction: row;
  align-content: space-between;
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
