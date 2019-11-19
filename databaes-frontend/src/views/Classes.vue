<template>
  <div class="classes body-with-sidebar">
    <section id="sidebar">
      <ul>
        <li
          v-for="classType in classes"
          :key="classType.id"
          :id="classType.id"
          :name="classType.name"
          class="assignment"
          :class="{ selected: classType.id == selectedClassNumber }"
          @click="selectClass(classType.id)">
          {{ classType.name }}
          <ul class="assignments">
            <li
              v-for="assignment in classType.assignments"
              :key="assignment.id"
              :id="assignment.id"
              :name="assignment.name"
              class="assignment"
              :class="{ selected: assignment.id == selectedAssignmentNumber }"
              @click="selectedAssignmentNumber = assignment.id">
              {{ assignment.name }}
            </li>
          </ul>
        </li>
      </ul>
    </section>
    <section class="classview">
      <h1> {{ selectedClass.name }} </h1>
      <div class="timeDisplay">
        <h3> Total time spent: <strong>{{ selectedClass.totalTime }}</strong> hours </h3>
        <h3> Average time spent per day: <strong>{{ selectedClass.averageTime }}</strong> hours </h3>
      </div>
      <div class="graph">
        Graph will go here
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'home',
  components: {
  },
  props: {
    classes: Array
  },
  data: function () {
    return {
      selectedClassNumber: 0,
      selectedAssignmentNumber: 0
    }
  },
  methods: {
    selectClass: function (classId) {
      if (this.selectedClassNumber !== classId) {
        this.selectedClassNumber = classId
        this.selectedAssignmentNumber = 0
      }
    }
  },
  computed: {
    selectedClass: function () {
      return this.classes[this.selectedClassNumber].assignments[this.selectedAssignmentNumber]
    }
  }
}
</script>

<style scoped>
.classes {
  display: flex;
  flex-direction: row;
}

li {
  padding-top: 2px;
  padding-bottom: 2px;
}

#sidebar > ul {
  list-style-position: inside;
  padding-left: 0;
}

#sidebar > ul > li {
  list-style-type: disclosure-closed;
  cursor: pointer;
}

#sidebar > ul > li > ul {
  display: none;
}

#sidebar > ul > li.selected {
  list-style-type: disclosure-open;
  font-weight: bold;
  cursor: default;
}

#sidebar > ul > li.selected > ul {
  display: block;
  font-weight: normal;
  cursor: pointer;
}

#sidebar > ul > li > ul > li.selected {
  font-weight: bold;
  cursor: default;
}

.classview {
  width: 1000px;
  margin: auto;
  padding-left: 20px;
}

.timeDisplay {
  display: flex;
  justify-content: space-between;
}

.timeDisplay > h3 {
  text-align: center;
}

.timeDisplay > h3 > strong {
  position: relative;
  top: 0.25em;
  font-size: 3em;
  text-align: center;
}

@media only screen and (min-width: 1001px) {
  .timeDisplay {
    flex-direction: row;
  }

  .timeDisplay > h3 {
    margin-left: 20px;
    margin-right: 20px;
  }
}

@media only screen and (max-width: 1000px) {
  .timeDisplay {
    flex-direction: column;
  }

  .timeDisplay > h3 {
    margin-left: 5px;
    margin-right: 5px;
    margin-top: 10px;
    margin-bottom: 10px;
  }
}

.graph {
  max-width: 540px;
  height: 240px;
  background-color: gray;
  color: #FFFFFF;
  padding: 30px;
  font-size: 2em;
  margin: auto;
  margin-bottom: 30px;
}
</style>
