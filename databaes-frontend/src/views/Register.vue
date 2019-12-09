<template>
  <div class="register">
    <h1>Register</h1>
    <form v-on:submit.prevent="register">
      <fieldset>
        <label for="username">Username:</label>
        <input type="text" v-model="username" id="username"/>
      </fieldset>
      <fieldset>
        <label for="email">Email:</label>
        <input type="text" v-model="email" id="email"/>
      </fieldset>
      <fieldset>
        <label for="name">Name:</label>
        <input type="text" v-model="name" id="name"/>
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
import axios from 'axios'

export default {
  name: 'register',
  components: {
  },
  data: function () {
    return {
      username: '',
      password: '',
      passwordAgain: '',
      email: '',
      name: '',
      rememberMe: true
    }
  },
  methods: {
    register: function () {
      // TODO: data verification
      // TODO: remember me

      const payload = {
        username: this.username,
        email: this.email,
        password: this.password,
        name: this.name
      }

      axios.post('v1/users/', payload)
        .then((response) => {
          return this.$store.dispatch('obtainToken', {
            email: this.email,
            password: this.password,
            rememberMe: this.rememberMe
          })
        }).then(() => {
          this.$emit('pull-data', () => { this.$router.push('/profile') })
        })
        .catch((error) => {
          this.$emit('show-error', error)
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
