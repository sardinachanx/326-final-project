<template>
  <div class="planner">
    <h1> Homework Planner </h1>
    <p> Plan your homework here </p>
    <AddHomeworkForm v-on:addHomework="addHomework"/>
    <ul>
      <HomeworkEntry v-for="assignment in assignments" :key="assignment.id" :id="assignment.id" :name="assignment.name" class="assignment" v-on:removeHomework="removeHomework"/>
    </ul>
  </div>
</template>

<script>
import AddHomeworkForm from '@/components/AddHomeworkForm.vue'
import HomeworkEntry from '@/components/HomeworkEntry.vue'

export default {
  name: 'homeworkplanner',
  components: {
    AddHomeworkForm,
    HomeworkEntry
  },
  data: function () {
    return {
      assignments: [
        {
          name: 'Some homework',
          id: 0
        },
        {
          name: 'Some other homework',
          id: 1
        }
      ],
      highestId: 1
    }
  },
  methods: {
    addHomework: function (name) {
      this.assignments.push({
        name: name,
        id: ++this.highestId
      })
    },
    removeHomework: function (id) {
      console.log('Removing ' + id)
      for (let i in this.assignments) {
        let assignment = this.assignments[i]
        if (assignment.id === id) {
          this.assignments.splice(i, 1)
          break
        }
      }
    }
  }
}
</script>

<style scoped>
ul {
  text-align: left;
}

.planner {
  max-width: 500px;
}
</style>
