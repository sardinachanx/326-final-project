<template>
  <form class="enroll_course">
    <h1> Enroll in a new class? </h1>
    <fieldset>
      <div>
        <label for="name">Course Name</label>
        <input name="name" type="text" v-model="name">
      </div>
      <div>
        <label for="number">Course Number</label>
        <input name="number" type="number" v-model="number">
      </div>
      <div>
        <label for="subject">Course Subject</label>
        <select name="subject" v-model="subject">
          <option value="" disabled> Select One </option>
          <option v-for="subject in courseSubjects" :key="subject.value" v-bind:value="subject.value">{{ subject.value + " — " + subject.display_name }}</option>
        </select>
      </div>
    </fieldset>
    <fieldset>
      <label for="year">Year</label>
      <input name="year" type="number" v-model="year">
      <br />
      <input name="term" type="radio" v-model="term" value="F" id="F">
      <label for="F">Fall</label>
      <input name="term" type="radio" v-model="term" value="S" id="S">
      <label for="S">Spring</label>
    </fieldset>
    <button v-on:click="enrollCourse" type="button"> Add Course </button>
  </form>
</template>

<script>
import axios from 'axios'
import courseSubjects from '@/assets/courses.json'

export default {
  name: 'EnrollCourseForm',
  data: function () {
    return {
      name: '',
      number: null,
      subject: '',
      year: new Date().getFullYear(),
      term: new Date().getMonth() < 6 ? 'S' : 'F'
    }
  },
  methods: {
    enrollCourse: function () {
      console.log('enrolling ' + this.name + ' for ' + this.term + this.year)

      // TODO: check if course already exists

      // create the course
      const payload = {
        name: this.name,
        course_number: this.number,
        subject: this.subject,
        year: this.year,
        term: this.term
      }

      axios.post('v1/courses/', payload, {
        headers: { 'Authorization': 'Bearer ' + this.$store.state.access }
      })
        .then((response) => {
          // enroll in the course
          let courseId = response.data.id
          const payload = {
            course: courseId,
            year: this.year,
            term: this.term
          }

          return axios.post('v1/enrollment/', payload, {
            headers: { 'Authorization': 'Bearer ' + this.$store.state.access }
          })
        })
        .then((response) => {
          this.$emit('pull-data', () => {})
        })
        .catch((error) => {
          // TODO: actually catch it
          this.$emit('show-error', error)
        })
    }
  },
  created () {
    this.courseSubjects = courseSubjects
  }
}
</script>

<style scoped>
.enroll_course {
  text-align: left;
  max-width: 600px;
}

form {
  display: flex;
  flex-direction: column;
  max-width: 50%;
  margin: 0 auto;
}

label {
  margin-right: 10px;
}

fieldset {
  margin: 10px;
  padding-top: 10px;
}
</style>
