/* eslint-disable */
import axios from 'axios'

const API_URL = '' //juanpa ip

export default () => {
    return axios.create({
        baseURL: `http://localhost:8081/`
    })
}