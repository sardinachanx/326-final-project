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
  props: {
    user: Object
  },
  methods: {
    enrollCourse: function () {
      console.log('enrolling ' + this.name + ' for ' + this.term + this.year)

      axios.get('v1/courses/', {
        headers: { 'Authorization': 'Bearer ' + this.$store.state.access }
      }).then((response) => {
        // if already enrolled in the course, enroll in this one, otherwise create the course

        let courses = response.data
        let existingCourse = this.getMatchingCourse(this.subject, this.number, courses)

        if (existingCourse === null) {
          // create the course

          return axios.post('v1/courses/', {
            name: this.name,
            course_number: this.number,
            subject: this.subject,
            year: this.year,
            term: this.term
          }, {
            headers: { 'Authorization': 'Bearer ' + this.$store.state.access }
          })
        } else {
          return Promise.resolve({
            data: {
              id: existingCourse.id
            }
          })
        }
      }).then((response) => {
        // check if already enrolled in the course
        let alreadyEnrolledCourse = this.getMatchingCourse(this.subject, this.number, this.user.courses)

        if (alreadyEnrolledCourse !== null) {
          return Promise.resolve()
        }

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
      }).then((response) => {
        this.$emit('pull-data', () => {})
        this.number = null
        this.subject = ''
        this.year = new Date().getFullYear()
        this.term = new Date().getMonth() < 6 ? 'S' : 'F'
        this.name = ''
      }).catch((error) => {
        this.$store.dispatch('showError', error)
      })
    },
    getMatchingCourse: function (courseSubject, courseNumber, courses) {
      let courseNames = courses.map((course) => { return course.subject + ' ' + course.course_number })
      console.log('checking for ' + courseSubject + ' ' + courseNumber + ' in ' + courseNames)
      for (let course of courses) {
        if ((course.course_number === courseNumber && course.subject === courseSubject) || (course.course_name !== undefined && course.course_name.startsWith(courseSubject + ' ' + courseNumber))) {
          return course
        }
      }

      return null
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
