<template>
  <div class="assignment">
    <h1>
      {{ selectedCourse.course_name }} - {{ selectedAssignment.type }} {{ selectedAssignment.number }}
    </h1>
    <div v-if="assignment !== null">
      <div class="timeDisplay">
        <h3> Total time spent: <strong>{{ Math.round(timeToHours(assignment.avg_total_hours)*10)/10 }}</strong> hours </h3>
        <h3>
          Average time spent per day:
          <strong>{{ Math.round(Object.values(assignment.avg_daily_hours).reduce((a, b) => timeToHours(a) + timeToHours(b), 0) / Object.values(assignment.avg_daily_hours).length * 10) / 10 }}</strong>
          hours
        </h3>
      </div>
      <div class="graph">
        Graph will go here
      </div>
      <AddDayEntryForm :assignmentId="this.assignment.id"  v-on:pull-data="$emit('pull-data', () => {})"/>
    </div>
    <div v-if="assignment === null">
      <h3> Loading... </h3>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import AddDayEntryForm from '@/components/AddDayEntryForm.vue'

export default {
  name: 'Assignment',
  props: {
    selectedAssignment: Object,
    selectedCourse: Object
  },
  data: function () {
    return {
      assignment: null,
      stats: null
    }
  },
  components: {
    AddDayEntryForm
  },
  methods: {
    loadAssignment: function () {
      axios.get('v1/assignments/' + this.selectedAssignment.id + '/', {
        headers: { 'Authorization': 'Bearer ' + this.$store.state.access }
      })
        .then((response) => {
          this.assignment = response.data
        })
        .catch((error) => {
          this.$store.dispatch('showError', error)
        })

      axios.get('v1/stats/', {
        headers: { 'Authorization': 'Bearer ' + this.$store.state.access }
      })
        .then((response) => {
          this.stats = response.data.user_stats.course_breakdown[this.selectedCourse.course].assignment_breakdown[this.selectedAssignment.id]
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
  },
  watch: {
    selectedAssignment: function () {
      this.loadAssignment()
    }
  },
  mounted: function () {
    this.loadAssignment()
  }
}
</script>

<style scoped>
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
