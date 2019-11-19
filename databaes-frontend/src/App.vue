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
    <router-view id="body" :classes="classes"/>
  </div>
</template>

<script>
export default {
  name: 'app',
  data: function () {
    return {
      classes: []
    }
  },
  mounted: function () {
    // TODO: load data from backend
    this.classes = [
      {
        name: 'COMPSCI 250',
        assignments: [
          {
            name: 'Problem Set 1',
            totalTime: 16,
            averageTime: 2,
            id: 0
          },
          {
            name: 'Problem Set 2',
            totalTime: 14,
            averageTime: 3,
            id: 1
          },
          {
            name: 'Midterm 1',
            totalTime: 30,
            averageTime: 15.5,
            id: 2
          }
        ],
        id: 0
      },
      {
        name: 'MATH 235',
        assignments: [
          {
            name: 'MyMathLab HW 1',
            totalTime: 2,
            averageTime: 2,
            id: 0
          },
          {
            name: 'MyMathLab HW 2',
            totalTime: 3,
            averageTime: 3,
            id: 1
          },
          {
            name: 'Midterm 1',
            totalTime: 5,
            averageTime: 2.5,
            id: 2
          },
          {
            name: 'Midterm 2',
            totalTime: 6,
            averageTime: 1.5,
            id: 3
          }
        ],
        id: 1
      },
      {
        name: 'MATH 235',
        assignments: [
        ],
        id: 2
      },
      {
        name: 'MATH 235',
        assignments: [
        ],
        id: 3
      },
      {
        name: 'MATH 235',
        assignments: [
        ],
        id: 4
      },
      {
        name: 'MATH 235',
        assignments: [
        ],
        id: 5
      },
      {
        name: 'MATH 235',
        assignments: [
        ],
        id: 6
      },
      {
        name: 'MATH 235',
        assignments: [
        ],
        id: 7
      },
      {
        name: 'MATH 235',
        assignments: [
        ],
        id: 8
      },
      {
        name: 'MATH 235',
        assignments: [
        ],
        id: 9
      },
      {
        name: 'MATH 235',
        assignments: [
        ],
        id: 10
      },
      {
        name: 'MATH 235',
        assignments: [
        ],
        id: 11
      },
      {
        name: 'MATH 235',
        assignments: [
        ],
        id: 12
      },
      {
        name: 'MATH 235',
        assignments: [
        ],
        id: 13
      },
      {
        name: 'MATH 235',
        assignments: [
        ],
        id: 14
      },
      {
        name: 'MATH 235',
        assignments: [
        ],
        id: 15
      },
      {
        name: 'MATH 235',
        assignments: [
        ],
        id: 16
      },
      {
        name: 'MATH 235',
        assignments: [
        ],
        id: 17
      },
      {
        name: 'MATH 235',
        assignments: [
        ],
        id: 18
      },
      {
        name: 'MATH 235',
        assignments: [
        ],
        id: 19
      },
      {
        name: 'MATH 235',
        assignments: [
        ],
        id: 20
      },
      {
        name: 'MATH 235',
        assignments: [
        ],
        id: 21
      },
      {
        name: 'MATH 235',
        assignments: [
        ],
        id: 22
      },
      {
        name: 'MATH 235',
        assignments: [
        ],
        id: 23
      },
      {
        name: 'MATH 235',
        assignments: [
        ],
        id: 24
      },
      {
        name: 'MATH 235',
        assignments: [
        ],
        id: 25
      }
    ]
  }
}
</script>

<style>
body {
  margin: 0;
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
