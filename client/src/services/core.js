import http from '@/config/http';
import lStorage from '@/config/lstorage';

export default {
  listDocuments(data) {
    return http.get('/api/documents', data);
  },
  searchDocuments(data) {
    return http.get('/api/search', data);
  },
  getSuggestions(data) {
    return http.get('/api/suggestions', data);
  },
  uploadDocument(data) {
    return http.post('/api/documents', data, {
      headers: {
        "Authorization": `Bearer ${lStorage.get("jwt")}`,
        'Content-Type': 'multipart/form-data'
      }
    })
  }
}
