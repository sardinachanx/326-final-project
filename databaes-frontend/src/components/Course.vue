<template>
  <div class="course">
    <h1>
      {{ selectedCourse.subject }} {{ selectedCourse.course_number }} {{ selectedCourse.name }}
    </h1>
    <h3>
      Average hours per week: {{ Math.round(timeToHours(stats.average_hours_per_week) * 10) / 10 }}
    </h3>
    <h3>
      Total hours: {{ Math.round(timeToHours(stats.total_hours) * 10) / 10 }}
    </h3>
    <AddAssignmentForm :courseId="selectedCourse.id" v-on:pull-data="$emit('pull-data', () => {})"/>
  </div>
</template>

<script>
import axios from 'axios'
import AddAssignmentForm from '@/components/AddAssignmentForm.vue'

export default {
  name: 'Course',
  props: {
    selectedCourse: Object
  },
  components: {
    AddAssignmentForm
  },
  data: function () {
    return {
      stats: null
    }
  },
  methods: {
    getStats: function () {
      axios.get('v1/stats/', {
        headers: { 'Authorization': 'Bearer ' + this.$store.state.access }
      })
        .then((response) => {
          this.stats = response.data.user_stats.course_breakdown[this.selectedCourse.id]
        })
        .catch((error) => {
          this.$store.dispatch('showError', error)
        })
    },
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
      let pattern = /(?:(\d+) days?, )?(\d+):(\d+):(\d+)/
      let groups = timeString.match(pattern)
      let time = 0
      time += groups[1] === undefined ? 0 : parseInt(groups[1]) * 24 // optional days
      time += parseInt(groups[2]) // hours
      time += parseInt(groups[3]) / 60 // minutes
      time += parseInt(groups[4]) / (60 * 60) // seconds
      return time
    }
  },
  watch: {
    selectedCourse: function () {
      this.getStats()
    }
  },
  mounted: function () {
    this.getStats()
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
