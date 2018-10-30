import Vue from 'vue'
import Vuetify from 'vuetify'
import 'material-design-icons-iconfont/dist/material-design-icons.css'
import Router from 'vue-router'
import Login from '@/components/Login'
import UserView from '@/components/UserView'
import TicketsView from '@/components/TicketsView'
import RegisterView from '@/components/RegisterView'
import 'vuetify/dist/vuetify.min.css' // Ensure you are using css-loader

Vue.use(Router)
Vue.use(Vuetify)
Vue.component('tickets-component', TicketsView)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/userView',
      name: 'UserView',
      component: UserView
    },
    {
      path: '/registerView',
      name: 'RegisterView',
      component: RegisterView
    }
  ]
})
