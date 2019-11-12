<template>
  <li class="homework_entry">
    <button v-on:click="$emit('removeHomework', id)" type="button">
      Complete
    </button>
    {{ name }}
  </li>
</template>

<script>
export default {
  name: 'AddHomeworkForm',
  props: {
    name: String,
    id: Number
  },
  data: function () {
    return {
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.homework_entry {
  display: block;
}
</style>
