// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'

Vue.config.productionTip = false;
Vue.prototype.$g_username = "";
Vue.prototype.$g_password = "";
Vue.prototype.$g_role = "";
Vue.prototype.$g_baseURL = "Url";


/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})