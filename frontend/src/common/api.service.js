import axios from "axios";

/*
Définition de l'ApiService
*/
const ApiService = {
  init() {
    axios.defaults.baseURL = import.meta.env.VITE_APP_API_URL;
    axios.defaults.withCredentials = true;
    axios.defaults.xsrfHeaderName = "X-CSRFToken";
    axios.defaults.xsrfCookieName = "csrftoken";
  },

  async query(resource, params) {
    return axios.get(resource + "/", { params });
  },

  async get(resource, slug = "") {
    return axios.get(`${resource}/${slug}`);
  },

  async post(resource, params) {
    return axios.post(resource + "/", params);
  },

  async update(resource, slug, params) {
    return axios.patch(`${resource}/${slug}/`, params);
  },

  async put(resource, params) {
    return axios.put(resource + "/", params);
  },

  async delete(resource, slug = "") {
    return axios.delete(resource + "/" + (slug == "" ? "" : slug + "/"));
  },
};

export default ApiService;
