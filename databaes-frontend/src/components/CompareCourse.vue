<template>
  <div class="course">
    <h1>
      {{ selectedCourse.subject }} {{ selectedCourse.course_number }} - {{ selectedCourse.name }}
    </h1>
    <h3> Weekly hours: {{ Math.round(timeToHours(selectedCourse.average_weekly_hours)*10)/10 }} </h3>
  </div>
</template>

<script>
export default {
  name: 'CompareCourse',
  props: {
    selectedCourse: Object
  },
  methods: {
    timeToHours: function (timeString) {
      if (timeString === null || timeString === undefined) {
        return null
      }
      if (Number.isFinite(timeString)) {
        return timeString
      }
      if (timeString === '0.0') {
        return 0
      }
      console.log(timeString)
      let pattern = /(?:(\d+) days?, )?(\d+):(\d+):(\d+)/
      let groups = timeString.match(pattern)
      console.log(groups)
      let time = 0
      time += groups[1] === undefined ? 0 : parseInt(groups[1]) * 24 // optional days
      time += parseInt(groups[2]) // hours
      time += parseInt(groups[3]) / 60 // minutes
      time += parseInt(groups[4]) / (60 * 60) // seconds
      return time
    }
  }
}
</script>

<style scoped>
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
