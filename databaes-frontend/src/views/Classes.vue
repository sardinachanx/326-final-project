<template>
  <div class="classes body-with-sidebar">
    <ClassesSidebar :classes="classes" :selectedAssignmentNumber="selectedAssignmentNumber" :selectedClassNumber="selectedClassNumber" @selectClass="selectClass" @selectAssignment="selectAssignment"/>
    <section class="classview">
      <Assignment
        v-if="selectedAssignment != null"
        :selectedAssignment="selectedAssignment"
        :selectedClass="selectedClass"
        />
      <Class
        v-if="selectedAssignment == null"
        :selectedClass="selectedClass"
        />
    </section>
  </div>
</template>

<script>
import Assignment from '@/components/Assignment.vue'
import Class from '@/components/Class.vue'
import ClassesSidebar from '@/components/ClassesSidebar.vue'

export default {
  name: 'home',
  components: {
    Assignment,
    Class,
    ClassesSidebar
  },
  props: {
    classes: Array
  },
  data: function () {
    return {
      selectedClassNumber: 0,
      selectedAssignmentNumber: -1
    }
  },
  methods: {
    selectClass: function (classId) {
      this.selectedClassNumber = classId
      this.selectedAssignmentNumber = -1
    },
    selectAssignment: function (assignmentId) {
      this.selectedAssignmentNumber = assignmentId
    }
  },
  computed: {
    selectedClass: function () {
      return this.classes[this.selectedClassNumber]
    },
    selectedAssignment: function () {
      if (this.selectedAssignmentNumber >= 0) {
        return this.selectedClass.assignments[this.selectedAssignmentNumber]
      } else {
        return null
      }
    }
  }
}
</script>

<style scoped>
.classes {
  display: flex;
  flex-direction: row;
}

.classview {
  width: 1000px;
  margin: auto;
  padding-left: 20px;
}
</style>
