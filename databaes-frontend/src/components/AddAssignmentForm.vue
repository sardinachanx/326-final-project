<template>
  <form class="add_assignment">
    <h2> Add an assignment? </h2>
    <fieldset>
      <div>
        <label for="number">Assignment Number</label>
        <input name="number" type="number" v-model="number">
      </div>
      <div>
        <label for="assignedDate">Assigned Date</label>
        <input name="assignedDate" type="date" v-model="assignedDate">
      </div>
      <div>
        <label for="dueDate">Due Date</label>
        <input name="dueDate" type="date" v-model="dueDate">
      </div>
      <div>
        <label for="type">Type</label>
        <select name="type" v-model="type">
          <option value="" disabled> Select One </option>
          <option v-for="assignmentType in assignmentTypes" :key="assignmentType.value" v-bind:value="assignmentType.value">{{ assignmentType.display_name }}</option>
        </select>
      </div>
    </fieldset>
    <button v-on:click="addAssignment" type="button"> Add Assignment </button>
  </form>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AddAssignmentForm',
  data: function () {
    return {
      number: null,
      type: '',
      assignedDate: null,
      dueDate: null
    }
  },
  props: {
    courseId: Number
  },
  methods: {
    addAssignment: function () {
      console.log('adding ' + this.type + ' ' + this.number)

      // TODO: check if assignment already exists

      // create the assignment
      const payload = {
        number: this.number,
        type: this.type,
        assigned_date: this.assignedDate,
        due_date: this.dueDate,
        course: this.courseId
      }

      axios.post('v1/assignments/', payload, {
        headers: { 'Authorization': 'Bearer ' + this.$store.state.access }
      })
        .then((response) => {
          this.$emit('pull-data', () => {})
        })
        .catch((error) => {
          this.$store.dispatch('showError', error)
        })
    }
  },
  created () {
    this.assignmentTypes = [
      {
        'value': 'PS',
        'display_name': 'Problem Set'
      },
      {
        'value': 'QZ',
        'display_name': 'Quiz'
      },
      {
        'value': 'EX',
        'display_name': 'Exam'
      },
      {
        'value': 'PR',
        'display_name': 'Presentation'
      },
      {
        'value': 'ES',
        'display_name': 'Essay'
      },
      {
        'value': 'PJ',
        'display_name': 'Project'
      }
    ]
  }
}
</script>

<style scoped>
.add_assignment {
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
