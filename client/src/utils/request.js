import axios from 'axios';

const service = axios.create({
  baseURL: process.env.VUE_APP_BASE_API_ENDPOINT,
  timeout: 1000,
  withCredentials: false,
});

export default {
  getCatalog() {
    return service.get('/catalog');
  },
  
};
