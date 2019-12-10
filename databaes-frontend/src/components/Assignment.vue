<template>
  <div class="assignment">
    <h1>
      {{ selectedCourse.subject }} {{ selectedCourse.course_number }} {{ selectedCourse.name }} - {{ assignmentTypes[selectedAssignment.type] }} {{ selectedAssignment.number }}
    </h1>
    <h2> {{ selectedAssignment.assigned_date }} - {{ selectedAssignment.due_date }} </h2>
    <div v-if="assignment !== null" class="innerView">
      <div class="timeDisplay">
        <div class="times">
          <h3> Total time: <strong>{{ totalTimeSpent }}</strong> hours </h3>
          <h3>
            Average time per day:
            <strong>{{ averageTimePerDay }}</strong>
            hours
          </h3>
        </div>
        <v-chart v-bind:chartData="chartData" class="graph" v-if="totalTimeSpent !== 0"></v-chart>
      </div>
      <AddDayEntryForm :assignmentId="this.assignment.id"  v-on:pull-data="$emit('pull-data', () => {})" class="form"/>
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
      stats: null,
      assignmentTypes: {
        ES: 'Essay',
        EX: 'Exam',
        PJ: 'Project',
        PR: 'Presentation',
        PS: 'Problem Set',
        QZ: 'Quiz'
      }
    }
  },
  components: {
    AddDayEntryForm
  },
  computed: {
    chartData: function () {
      let data = Object.entries(this.assignment.avg_daily_hours)
      data = data.filter(([date, time]) => {
        return new Date(date) <= Date.now()
      })
      data = data.map(([date, time]) => {
        return { date: date.substring(5).replace('-', '/'), time: this.timeToHours(time) }
      })

      console.log(data)

      return {
        chartType: 'vBarChart',
        selector: 'vBarChart',
        title: 'Hours per Day',
        width: 400,
        height: 200,
        metric: ['time'],
        dim: 'date',
        label: false,
        data: data
      }
    },
    averageTimePerDay: function () {
      return Math.round(Object.values(this.assignment.avg_daily_hours).reduce((a, b) => this.timeToHours(a) + this.timeToHours(b), 0) / Object.values(this.assignment.avg_daily_hours).length * 10) / 10
    },
    totalTimeSpent: function () {
      return Math.round(this.timeToHours(this.assignment.avg_total_hours) * 10) / 10
    }
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
          let courseInfo = response.data.user_stats.course_breakdown[this.selectedCourse.course]
          if (courseInfo === undefined) {
            this.stats = undefined
            return
          }
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
    selectedAssignment: function () {
      this.loadAssignment()
    }
  },
  mounted: function () {
    this.loadAssignment()
  }
}
</script>

<style>
.classview {
  width: 1000px;
  margin: auto;
  padding-left: 20px;
}

.innerView {
  text-align: center;
}

.timeDisplay {
  margin: auto;
  display: flex;
  justify-content: space-between;
}

.times > h3 {
  text-align: center;
}

.times > h3 > strong {
  position: relative;
  top: 0.25em;
  font-size: 3em;
  text-align: center;
  color: #038288;
}

@media only screen and (min-width: 1001px) {
  .timeDisplay {
    flex-direction: row;
  }

  .times > h3 {
    margin-left: 20px;
    margin-right: 20px;
  }
}

@media only screen and (max-width: 1000px) {
  .timeDisplay {
    flex-direction: column;
  }

  .times > h3 {
    margin-left: 5px;
    margin-right: 5px;
    margin-top: 10px;
    margin-bottom: 10px;
  }
}

.graph {
  margin: 0 auto;
}

.form {
  margin-bottom: 30px;
}

svg :nth-child(2) > g > text {
  transform: rotate(65deg) translateX(15pt) translateY(-6pt)
}

svg {
  transform: scale(1.4);
  padding: 30px;
}

rect {
  fill: #038288;
}
</style>
