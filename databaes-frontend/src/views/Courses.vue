<template>
  <div class="courses body-with-sidebar">
    <CoursesSidebar
      :courses="user.courses"
      :selectedAssignmentNumber="selectedAssignmentNumber"
      :selectedCourseNumber="selectedCourseNumber"
      @selectCourse="selectCourse" />
    <section class="courseview">
      <Assignment
        v-if="selectedAssignment != null"
        :selectedAssignment="selectedAssignment"
        :selectedCourse="selectedCourse"
        v-on:pull-data="$emit('pull-data', () => {}); "
        />
      <Course
        v-if="selectedAssignment == null && selectedCourse != null"
        :selectedCourse="selectedCourse"
        v-on:pull-data="$emit('pull-data', () => {}); selectCourse(selectedCourseNumber)"
        />
      <EnrollCourseForm
        v-if="selectedAssignment == null && selectedCourse == null"
        :user="user"
        v-on:pull-data="$emit('pull-data', () => {})"
        />
    </section>
  </div>
</template>

<script>
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
    user: Object,
    specificCourses: Array
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

      this.selectedCourseNumber = courseId
      this.selectedAssignmentNumber = assignmentId
    }
  },
  computed: {
    selectedCourse: function () {
      console.log('updating selected course')
      if (this.user.courses === undefined || this.user.courses.length === 0 || this.selectedCourseNumber === -1) {
        return null
      }
      for (let course of this.user.courses) {
        if (course.id === this.selectedCourseNumber) {
          return course
        }
      }
      return null
    },
    selectedAssignment: function () {
      console.log('Updating assignment with ' + this.selectedAssignmentNumber)
      if (this.selectedCourse === null || this.selectedCourse.assignments === undefined || this.selectedCourse.assignments.length === 0 || this.selectedAssignmentNumber === -1) {
        console.log('selectedCourse.assignments is undefined')
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
