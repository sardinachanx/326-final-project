<template>
  <div class="course">
    <h1>
      {{ selectedCourse.subject }} {{ selectedCourse.course_number }} {{ selectedCourse.name }}
    </h1>
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
          this.stats = response.data.user_stats.course_breakdown[this.selectedCourse.course]
        })
        .catch((error) => {
          this.$store.dispatch('showError', error)
        })
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
