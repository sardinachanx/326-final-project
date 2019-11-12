<template>
  <form class="add_homework_form">
    <input name="name" type="text" v-model="name">
    <button v-on:click="$emit('addHomework', name)" type="button"> Add Homework </button>
  </form>
</template>

<script>
export default {
  name: 'AddHomeworkForm',
  data: function () {
    return {
      name: ''
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
