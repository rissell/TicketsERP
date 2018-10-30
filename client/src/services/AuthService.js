/* eslint-disable */

import Api from '@/services/Api'

export default {
    login (credentials) {
        return Api().post('login', credentials)
    }
}

// AuthService.login({
//     email: 'rosa@odoo.com',
//     password: 'labweb'
// })