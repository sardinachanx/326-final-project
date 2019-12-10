<template>
  <div class="courses body-with-sidebar">
    <CompareSidebar
      :courses="courses"
      :selectedCourseNumber="selectedCourseNumber"
      @selectCourse="selectCourse" />
    <section class="courseview">
      <CompareCourse
        v-if="selectedCourse != null"
        :selectedCourse="selectedCourse"
        v-on:pull-data="$emit('pull-data', () => {}); selectCourse(selectedCourseNumber)"
        />
    </section>
  </div>
</template>

<script>
import CompareCourse from '@/components/CompareCourse.vue'
import CompareSidebar from '@/components/CompareSidebar.vue'

export default {
  name: 'compare',
  components: {
    CompareCourse,
    CompareSidebar
  },
  props: {
    courses: Array
  },
  data: function () {
    return {
      selectedCourseNumber: -1
    }
  },
  methods: {
    selectCourse: function (courseId) {
      this.selectedCourseNumber = courseId
    }
  },
  computed: {
    selectedCourse: function () {
      if (this.courses === undefined || this.courses.length === 0 || this.selectedCourseNumber === -1) {
        return null
      }
      for (let course of this.courses) {
        if ((course.course || course.id) === this.selectedCourseNumber) {
          return course
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
