import Vue from 'vue'
import Vuetify from 'vuetify'
import 'material-design-icons-iconfont/dist/material-design-icons.css'
import Router from 'vue-router'
import login from '@/components/login'
import userView from '@/components/userView'
import ticketsViewOngoing from '@/components/ticketsViewOngoing'
import ticketsViewPending from '@/components/ticketsViewPending'
import ticketsViewFixed from '@/components/ticketsViewFixed'
import adminView from '@/components/adminView'
import maintenaceDashboard from '@/components/maintenanceDashboardView'
import 'vuetify/dist/vuetify.min.css' // Ensure you are using css-loader

Vue.use(Router);
Vue.use(Vuetify);
Vue.component('ongoing-tickets-component', ticketsViewOngoing);
Vue.component('pending-tickets-component', ticketsViewPending);
Vue.component('fixed-tickets-component', ticketsViewFixed);

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/login',
      name: 'login',
      component: login
    },
    {
      path: '/user',
      name: 'userView',
      component: userView
    },
    {
      path: '/admin',
      name: 'adminView',
      component: adminView
    },
    {
      path: '/maintenance',
      name: 'maintenace-dashboard',
      component: maintenaceDashboard
    }
  ]
})
