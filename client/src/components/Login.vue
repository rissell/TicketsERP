<template>
    <div>
    <v-container>
        <v-layout row class="text-xs-center">
        <v-flex xs3>
          <v-card class="loginBackground" height="500px">
            <v-img src="http://www.praxya.com/wp-content/uploads/2018/09/logo-odoo-couleur_0cf0a14c.png">
          </v-img>
            </v-card>
        </v-flex>
        <v-flex xs4 class="grey lighten-4">
            <v-container style="position: relative;top: 13%;" class="text-xs-center">
            <v-card flat>
                <v-card-title primary-title>
                <h4>Login</h4>
                </v-card-title>
                <v-form>
                <v-text-field prepend-icon="person" name="Username" label="Username" v-model="email"></v-text-field>
                <v-text-field prepend-icon="lock" name="Password" label="Password" type="password" v-model="password"></v-text-field>
                <v-card-actions>
                <v-btn @click="login" primary large block>Login</v-btn>
                </v-card-actions>
                </v-form>
            </v-card>
            </v-container>
        </v-flex>
        </v-layout>
    </v-container>
    </div>
</template>

<script>

import AuthService from '@/services/AuthService'
export default {
  data () {
    return {
      email: '',
      password: ''
    }
  },
  methods: {
    async login () {
      const response = await AuthService.login({
        email: this.email,
        password: this.password
      })
      console.log(response.data)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .loginBackground {
    background-image: url('http://www.praxya.com/wp-content/uploads/2018/09/logo-odoo-couleur_0cf0a14c.png');
  }

</style>
