<template>
  <div class="courses body-with-sidebar">
    <CoursesSidebar :courses="user.profile.courses" :selectedAssignmentNumber="selectedAssignmentNumber" :selectedCourseNumber="selectedCourseNumber" @selectCourse="selectCourse" @selectAssignment="selectAssignment"/>
    <section class="courseview">
      <Assignment
        v-if="selectedAssignment != null"
        :selectedAssignment="selectedAssignment"
        :selectedCourse="selectedCourse"
        />
      <Course
        v-if="selectedAssignment == null && selectedCourse != null"
        :selectedCourse="selectedCourse"
        />
      <EnrollCourseForm
        v-if="selectedAssignment == null && selectedCourse == null"
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
    user: Object
  },
  data: function () {
    return {
      selectedCourseNumber: 0,
      selectedAssignmentNumber: -1
    }
  },
  methods: {
    selectCourse: function (courseId) {
      this.selectedCourseNumber = courseId
      this.selectedAssignmentNumber = -1
    },
    selectAssignment: function (assignmentId) {
      this.selectedAssignmentNumber = assignmentId
    }
  },
  computed: {
    selectedCourse: function () {
      if (this.user.profile.courses === undefined || this.user.profile.courses.length < this.selectedCourseNumber) {
        return null
      }
      return this.user.profile.courses[this.selectedCourseNumber]
    },
    selectedAssignment: function () {
      if (this.selectedAssignmentNumber >= 0) {
        return this.selectedCourse.assignments[this.selectedAssignmentNumber]
      } else {
        return null
      }
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
