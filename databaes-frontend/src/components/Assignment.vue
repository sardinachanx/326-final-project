<template>
  <div class="assignment">
    <h1>
      {{ selectedClass.name }} - {{ selectedAssignment.name }}
    </h1>
    <div class="timeDisplay">
      <h3> Total time spent: <strong>{{ selectedAssignment.totalTime }}</strong> hours </h3>
      <h3>
        Average time spent per day:
        <strong>{{ selectedAssignment.averageTime }}</strong>
        hours
      </h3>
    </div>
    <div class="graph">
      Graph will go here
    </div>
  </div>
</template>

<script>
export default {
  name: 'Assignment',
  props: {
    selectedAssignment: Object,
    selectedClass: Object
  }
}
</script>

<style scoped>
.classview {
  width: 1000px;
  margin: auto;
  padding-left: 20px;
}

.timeDisplay {
  display: flex;
  justify-content: space-between;
}

.timeDisplay > h3 {
  text-align: center;
}

.timeDisplay > h3 > strong {
  position: relative;
  top: 0.25em;
  font-size: 3em;
  text-align: center;
}

@media only screen and (min-width: 1001px) {
  .timeDisplay {
    flex-direction: row;
  }

  .timeDisplay > h3 {
    margin-left: 20px;
    margin-right: 20px;
  }
}

@media only screen and (max-width: 1000px) {
  .timeDisplay {
    flex-direction: column;
  }

  .timeDisplay > h3 {
    margin-left: 5px;
    margin-right: 5px;
    margin-top: 10px;
    margin-bottom: 10px;
  }
}

.graph {
  max-width: 540px;
  height: 240px;
  background-color: gray;
  color: #FFFFFF;
  padding: 30px;
  font-size: 2em;
  margin: auto;
  margin-bottom: 30px;
}
</style>
