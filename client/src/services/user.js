import http from '@/config/http';
import lStorage from '@/config/lstorage';

export default {
  login(data) {
    return http.post('/api/login', data);
  },
  signup(data) {
    return http.post('/api/registration', data);
  },
  logout() {
    return http.post('/api/logout', null, {
      headers: {
        "Authorization": `Bearer ${lStorage.get("jwt")}`
      }
    });
  },
  getUserProfile() {
    return http.get('/api/user/profile', {
      headers: {
        "Authorization": `Bearer ${lStorage.get("jwt")}`
      }
    })
  }

}
