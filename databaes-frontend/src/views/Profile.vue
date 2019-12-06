<template>
  <div class="profile">
    <h1>Profile</h1>
    <form v-if="true">
      <p>
        Username: {{ user.username }}
      </p>
      <p>
        Email: {{ user.email }}
      </p>
      <p>
        Name: {{ user.name }}
      </p>
    </form>
  </div>
</template>

<script>
export default {
  name: 'profile',
  components: {
  },
  props: {
    user: Object
  }
}
</script>

<style scoped>
.profile {
  text-align: left;
  max-width: 600px;
}

h1 {
  text-align: center;
}
</style>
