<template>
  <section id="sidebar" v-if="courses !== undefined && course !== null">
    <h3
      :class="{ course_selector: selectedCourseNumber !== -1 }"
      @click="$emit('selectCourse', -1)"
      > My Courses </h3>
    <ul v-if="courses !== undefined && courses !== null">
      <li
        :class="{ selected: selectedCourseNumber === -1, selectedOnly: selectedCourseNumber == -1 && selectedAssignmentNumber == -1 }"
        style="list-style-type: none;"
        @click="$emit('selectCourse', -1)"
        > <div> Enroll in more courses </div> </li>
      <li
        v-for="course in courses"
        :key="course.id"
        class="assignment"
        :class="{ selected: course.id == selectedCourseNumber, selectedOnly: course.id == selectedCourseNumber && selectedAssignmentNumber == -1 }"
        >
        <div
          @click="$emit('selectCourse', course.id)"
          style="display: inline; cursor: pointer;">
          {{ course.subject + ' ' + course.course_number + ' ' + course.name }}
        </div>
        <ul class="assignments">
          <li
            v-for="assignment in course.assignments"
            :key="assignment.id"
            class="assignment"
            :class="{
              selected: assignment.id == selectedAssignmentNumber
            }"
            @click="$emit('selectCourse', course.id, assignment.id)">
            {{ assignmentTypes[assignment.type] }} {{ assignment.number }}
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
  },
  data: function () {
    return {
      assignmentTypes: {
        ES: 'Essay',
        EX: 'Exam',
        PJ: 'Project',
        PR: 'Presentation',
        PS: 'Problem Set',
        QZ: 'Quiz'
      }
    }
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
}

#sidebar > ul > li > div {
  cursor: pointer;
  text-decoration: underline;
}

#sidebar > ul > li > ul {
  display: none;
}

#sidebar > ul > li.selected {
  list-style-type: disclosure-open;
  font-weight: bold;
}

#sidebar > ul > li.selectedOnly > div {
  cursor: default;
  text-decoration: none;
}

#sidebar > ul > li.selected > ul {
  display: block;
  font-weight: normal;
  cursor: pointer;
}

#sidebar > ul > li.selected > ul > li {
  text-decoration: underline;
}

#sidebar > ul > li > ul > li.selected {
  font-weight: bold;
  cursor: default;
  text-decoration: none;
}
</style>
