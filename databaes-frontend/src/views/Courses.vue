<template>
  <div class="courses body-with-sidebar">
    <CoursesSidebar
      :courses="user.courses"
      :selectedAssignmentNumber="selectedAssignmentNumber"
      :selectedCourseNumber="selectedCourseNumber"
      @selectCourse="selectCourse"
      @selectAssignment="selectAssignment"/>
    <section class="courseview">
      <Assignment
        v-if="selectedAssignment != null"
        :selectedAssignment="selectedAssignment"
        :selectedCourse="selectedCourse"
        v-on:pull-data="$emit('pull-data', () => {}); selectCourse(selectedCourseNumber, selectedAssignmentNumber)"
        />
      <Course
        v-if="selectedAssignment == null && selectedCourse != null"
        :selectedCourse="selectedCourse"
        v-on:pull-data="$emit('pull-data', () => {}); selectCourse(selectedCourseNumber)"
        />
      <EnrollCourseForm
        v-if="selectedAssignment == null && selectedCourse == null"
        v-on:pull-data="$emit('pull-data', () => {})"
        />
    </section>
  </div>
</template>

<script>
import axios from 'axios'

import Assignment from '@/components/Assignment.vue'
import Course from '@/components/Course.vue'
import CoursesSidebar from '@/components/CoursesSidebar.vue'
import EnrollCourseForm from '@/components/EnrollCourseForm.vue'

export default {
  name: 'courses',
  components: {
    Assignment,
    Course,
    CoursesSidebar,
    EnrollCourseForm
  },
  props: {
    user: Object
  },
  data: function () {
    return {
      selectedCourseNumber: -1,
      selectedAssignmentNumber: -1
    }
  },
  methods: {
    selectCourse: function (courseId, assignmentId) {
      if (assignmentId === undefined || assignmentId === null) {
        assignmentId = -1
      }
      if (courseId === -1) {
        this.selectedCourseNumber = -1
        this.selectedAssignmentNumber = -1
        return
      }

      axios.get('v1/courses/' + courseId + '/', {
        headers: { 'Authorization': 'Bearer ' + this.$store.state.access }
      })
        .then((response) => {
          this.selectedCourseNumber = courseId
          this.selectedAssignmentNumber = assignmentId

          this.$set(this.selectedCourse, 'assignments', response.data.assignments)
        })
        .catch((error) => {
          this.$emit('show-error', error)
        })
    },
    selectAssignment: function (assignmentId) {
      this.selectedAssignmentNumber = assignmentId
    }
  },
  computed: {
    selectedCourse: function () {
      if (this.user.courses === undefined || this.user.courses.length === 0 || this.selectedCourseNumber === -1) {
        return null
      }
      for (let course of this.user.courses) {
        if (course.course === this.selectedCourseNumber) {
          return course
        }
      }
      return null
    },
    selectedAssignment: function () {
      if (this.selectedCourse === null || this.selectedCourse.assignments === undefined || this.selectedCourse.assignments.length === 0 || this.selectedAssignmentNumber === -1) {
        return null
      }

      for (let assignment of this.selectedCourse.assignments) {
        if (assignment.id === this.selectedAssignmentNumber) {
          return assignment
        }
      }
      return null
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
</style>
