<template>
  <div class="login">
    <h1>Login</h1>
    <form v-on:submit.prevent="login()">
      <fieldset>
        <label for="email">Email:</label>
        <input type="text" v-model="email" id="email"/>
      </fieldset>
      <fieldset>
        <label for="password">Password:</label>
        <input type="password" v-model="password" id="password"/>
      </fieldset>
      <fieldset>
        <input v-model="rememberMe" type="checkbox" id="rememberMe"/>
        <label for="rememberMe">Remember Me</label>
      </fieldset>
      <button type="submit" id="submit">Login</button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'login',
  components: {
  },
  data: function () {
    return {
      email: '',
      password: '',
      rememberMe: true
    }
  },
  methods: {
    login: function () {
      // TODO: remember me
      // TODO: check for valid fields

      this.$store.dispatch('obtainToken', {
        email: this.email,
        password: this.password
      }).then(() => {
        this.$emit('pull-data', () => { this.$router.push('/profile') })
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
  padding-top: 10px;
}

h1 {
  text-align: center;
}
</style>
