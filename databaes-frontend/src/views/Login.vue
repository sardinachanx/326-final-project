<template>
  <div class="login">
    <h1>Login</h1>
    <form>
      <p>
        Username: {{user.username}}
      </p>
      <p>
        Email: {{user.email}}
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
  },
  methods: {
    login: function (username, password, rememberMe) {
      let redirect = this.$auth.redirect()

      this.$auth.login({
        data: {
          username: username,
          password: password
        },
        rememberMe: rememberMe,
        redirect: {
          name: redirect ? redirect.from.name : 'profile'
        }
      }).then(() => {}, (res) => {
        this.$emit('showError', res.data)
      })
    }
  }
}
</script>

<style scoped>
.login {
  text-align: left;
  max-width: 600px;
}

h1 {
  text-align: center;
}
</style>
