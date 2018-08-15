import Vue from 'vue'
import axios from "axios"
import lStorage from '../config/lstorage'

const instance = axios.create({
  baseURL: lStorage.get('serverApi'),
  timeout: 2000
});


instance.interceptors.request.use((request) => {
  // Vue.$Progress.start();
  return request;
}, (error) => {
  // NProgress.done();
  return Promise.reject(error);
});
instance.interceptors.response.use((response) => {
  // NProgress.done();
  return response;
}, (error) => {
  // NProgress.done();
  if (!error.response) {
    console.info('network error');
  } else{
    console.info(error.response)
    // Vue.store.dispatch('SET_AUTHENTICATED',false)
  }
    return Promise.reject(error);
});

export default instance
