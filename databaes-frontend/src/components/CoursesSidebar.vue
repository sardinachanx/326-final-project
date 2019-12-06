<template>
  <section id="sidebar">
    <h3> Courses </h3>
    <ul v-if="courses !== undefined && courses !== null">
      <li
        v-for="courseType in courses"
        :key="courseType.id"
        :id="courseType.id"
        :name="courseType.name"
        class="assignment"
        :course="{ selected: courseType.id == selectedCourseNumber }"
        >
        <div
          @click="$emit('selectCourse', courseType.id)"
          style="display: inline; cursor: pointer;">
          {{ courseType.name }}
        </div>
        <ul class="assignments">
          <li
            v-for="assignment in courseType.assignments"
            :key="assignment.id"
            :id="assignment.id"
            :name="assignment.name"
            class="assignment"
            :course="{
              selected: assignment.id == selectedAssignmentNumber
            }"
            @click="$emit('selectAssignment', assignment.id)">
            {{ assignment.name }}
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

#sidebar > ul {
  list-style-position: inside;
  padding-left: 0;
}

#sidebar > ul > li {
  list-style-type: disclosure-closed;
  cursor: pointer;
}

#sidebar > ul > li > ul {
  display: none;
}

#sidebar > ul > li.selected {
  list-style-type: disclosure-open;
  font-weight: bold;
  cursor: default;
}

#sidebar > ul > li.selected > ul {
  display: block;
  font-weight: normal;
  cursor: pointer;
}

#sidebar > ul > li > ul > li.selected {
  font-weight: bold;
  cursor: default;
}
</style>
