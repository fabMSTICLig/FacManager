/*
 * Copyright (C) 2020-2022 LIG Université Grenoble Alpes
 *
 *
 * This file is part of FacManager.
 *
 * FacManager is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
 *
 * FacManager is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along with FacManager. If not, see <https://www.gnu.org/licenses/>
 *
 * @author Germain Lemasson
*/

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
