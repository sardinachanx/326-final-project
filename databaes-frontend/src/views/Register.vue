<template>
  <div class="register">
    <h1>Register</h1>
    <form v-on:submit.prevent="register()">
      <fieldset>
        <label for="username">Username:</label>
        <input type="text" v-model="username" id="username"/>
      </fieldset>
      <fieldset>
        <label for="password">Password:</label>
        <input type="password" v-model="password" id="password"/>
      </fieldset>
      <fieldset>
        <label for="password">Password Again:</label>
        <input type="password" v-model="passwordAgain" id="passwordAgain"/>
      </fieldset>
      <fieldset>
        <input v-model="rememberMe" type="checkbox" id="rememberMe"/>
        <label for="rememberMe">Remember Me</label>
      </fieldset>
      <button type="submit" id="submit">Register</button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'register',
  components: {
  },
  data: function () {
    return {
      username: '',
      password: '',
      passwordAgain: '',
      rememberMe: true
    }
  },
  props: {
    user: Object
  },
  methods: {
    register: function (username, password, rememberMe) {
      let redirect = this.$auth.redirect()

      this.$auth.register({
        data: {
          username: username,
          password: password
        },
        autoLogin: true,
        rememberMe: rememberMe,
        redirect: {
          name: redirect ? redirect.from.name : 'profile'
        }
      }).then(() => {

      }, (res) => {
        this.$emit('showError', res.data)
      })
    }
  }
}
</script>

<style scoped>
.register {
  text-align: left;
  max-width: 600px;
}

form {
  display: flex;
  flex-direction: column;
  max-width: 50%;
  margin: 0 auto;
}

fieldset {
  margin: 10px;
  display: flex;
  justify-content: space-between;
}

h1 {
  text-align: center;
}
</style>
