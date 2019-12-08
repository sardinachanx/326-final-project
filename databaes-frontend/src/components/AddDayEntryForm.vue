<template>
  <form class="add_day_entry">
    <h2> Add a day entry? </h2>
    <fieldset>
      <div>
        <label for="date">Date</label>
        <input name="date" type="date"
          :value="date && date.toISOString().split('T')[0]"
          @input="date = $event.target.valueAsDate">
      </div>
      <div>
        <label for="duration">Number of hours</label>
        <input name="duration" type="number" v-model="duration">
      </div>
    </fieldset>
    <button v-on:click="addDayEntry" type="button"> Add Entry </button>
  </form>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AddDayEntryForm',
  data: function () {
    return {
      duration: null,
      date: new Date()
    }
  },
  props: {
    assignmentId: Number
  },
  methods: {
    addDayEntry: function () {
      console.log('adding ' + this.duration + ' for ' + this.date)

      // TODO: add the entry
      const payload = {
        assignment: this.assignmentId,
        date: this.date.toISOString().split('T')[0],
        duration: this.duration * 60 * 60
      }

      axios.post('v1/day-entries/', payload, {
        headers: { 'Authorization': 'Bearer ' + this.$store.state.access }
      })
        .then((response) => {
          this.$emit('pull-data', () => {})
        })
        .catch((error) => {
          // TODO: actually catch it
          this.$emit('show-error', error)
        })
    }
  }
}
</script>

<style scoped>
.add_day_entry {
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
