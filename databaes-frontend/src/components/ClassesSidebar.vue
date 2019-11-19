<template>
  <section id="sidebar">
    <ul>
      <li
        v-for="classType in classes"
        :key="classType.id"
        :id="classType.id"
        :name="classType.name"
        class="assignment"
        :class="{ selected: classType.id == selectedClassNumber }"
        >
        <div
          @click="$emit('selectClass', classType.id)"
          style="display: inline">
          {{ classType.name }}
        </div>
        <ul class="assignments">
          <li
            v-for="assignment in classType.assignments"
            :key="assignment.id"
            :id="assignment.id"
            :name="assignment.name"
            class="assignment"
            :class="{
              selected: assignment.id == selectedAssignmentNumber
            }"
            @click="$emit('selectAssignment', assignment.id)">
            {{ assignment.name }}
          </li>
        </ul>
      </li>
    </ul>
  </section>
</template>

<script>
export default {
  name: 'ClassesSidebar',
  props: {
    classes: Array,
    selectedClassNumber: Number,
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
