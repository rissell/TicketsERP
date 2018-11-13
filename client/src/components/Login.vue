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
                  <v-text-field prepend-icon="person" name="Username" label="Username" v-model="this.$g_username"></v-text-field>
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
import Vue from 'vue'
import axios from 'axios'
export default {
  data () {
    return {
      email: '',
      password: ''
    }
  },
  methods: {
    async login () {
        axios(
          {
            method: 'post',
            url: 'http://10.43.101.94:8080/login?user='+this.$g_username+'&psw='+this.password,
            //url: 'http://10.43.101.94:8080/login?user='+currentTicket.id+'&id='+this.currentTicket.id,
          }
        )
        .then(response => {
          console.log(response.data);
            if(response.data != "Deny"){
               if(response.data == 'user'){
                this.$router.push('/user');
               }else if(response.data == "staff"){
                this.$router.push('/maintenance');
               }else if(response.data == "admin"){
                 this.$router.push('/admin');
               }
            }else{
              alert("Invalid credentials.");
            }
        })
        .catch(error => {
          console.log(error);
        })
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
