<template>
  <div class="courses">
    <ul>
      <li
        v-for="course in courses"
        :key="course.id"
        >
        <h1>
          {{ course.subject }} {{ course.course_number }} - {{ course.name }}
        </h1>
        <h3>
          Weekly hours: {{ Math.round(timeToHours(course.average_weekly_hours)*10)/10 }}
        </h3>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'compare',
  props: {
    courses: Array
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
.courses {
  display: flex;
  flex-direction: row;
}

.courseview {
  width: 1000px;
  margin-left: auto;
  margin-right: auto;
  padding-left: 20px;
}

li {
  list-style-type: none;
}
</style>
