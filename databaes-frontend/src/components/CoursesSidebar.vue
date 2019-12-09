<template>
  <section id="sidebar">
    <h3
      :class="{ course_selector: selectedCourseNumber !== -1 }"
      @click="$emit('selectCourse', -1)"
      > Courses </h3>
    <ul v-if="courses !== undefined && courses !== null">
      <li
        :class="{ selected: selectedCourseNumber === -1 }"
        style="list-style-type: none;"
        @click="$emit('selectCourse', -1)"
        > Enroll in more courses </li>
      <li
        v-for="course in courses"
        :key="course.course"
        :id="course.course"
        :name="course.course_name"
        class="assignment"
        :class="{ selected: course.course == selectedCourseNumber }"
        >
        <div
          @click="$emit('selectCourse', course.course)"
          style="display: inline; cursor: pointer;">
          {{ course.course_name }}
        </div>
        <ul class="assignments">
          <li
            v-for="assignment in course.assignments"
            :key="assignment.id"
            :id="assignment.id"
            :name="assignment.name"
            class="assignment"
            :class="{
              selected: assignment.id == selectedAssignmentNumber
            }"
            @click="$emit('selectAssignment', assignment.id)">
            {{ assignment.type }} {{ assignment.number }}
          </li>
        </ul>
      </li>
    </ul>
    <p v-if="courses === undefined || courses === null">
      Not enrolled in any courses!
    </p>
  </section>
</template>

<script>
export default {
  name: 'CoursesSidebar',
  props: {
    courses: Array,
    selectedCourseNumber: Number,
    selectedAssignmentNumber: Number
  }
}
</script>

<style scoped>
li {
  padding-top: 2px;
  padding-bottom: 2px;
}

.course_selector {
  cursor: pointer;
}

#sidebar > ul {
  list-style-position: outside;
  padding-left: 16.7333px;
}

#sidebar > ul > li {
  list-style-type: disclosure-closed;
  cursor: pointer;
  text-decoration: underline;
}

#sidebar > ul > li > ul {
  display: none;
}

#sidebar > ul > li.selected {
  list-style-type: disclosure-open;
  font-weight: bold;
  cursor: default;
  text-decoration: none;
}

#sidebar > ul > li.selected > ul {
  display: block;
  font-weight: normal;
  cursor: pointer;
  text-decoration: underline;
}

#sidebar > ul > li > ul > li.selected {
  font-weight: bold;
  cursor: default;
  text-decoration: none;
}
</style>
