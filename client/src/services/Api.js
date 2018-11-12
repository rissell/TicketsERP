/* eslint-disable */
import axios from 'axios'

const API_URL = 'http://10.43.101.94:8080'; //juanpa ip

export default () => {
    return axios.create({
        baseURL: API_URL
    })
}
