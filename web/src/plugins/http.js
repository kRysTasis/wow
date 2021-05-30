import Vue from 'vue'
import axios from 'axios'
import router from '@/router'


export default {
    install: function (Vue, options) {
        const http = axios.create({
            baseURL: 'http://localhost:8000/',
            xsrfCookieName: 'csrftoken',
            xsrfHeaderName: 'X-CSRFTOKEN',
            timeout: 10000,
            headers: {
                common: {
                    'Content-Type': 'application/json;charset=utf-8',
                    'Access-Control-Allow-Origin': 'http://localhost:8000',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Access-Contorl-Allow-Headers': 'Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With, X-HTTP-Method-Override, Accept',
                    'Access-Control-Allow-Methods': 'PUT, DELETE, OPTIONS, POST, GET'
                }
            }
        })
        Vue.prototype.$axios = http
    }
}
