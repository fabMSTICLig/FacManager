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

import { createApp } from "vue";
import { createPinia } from "pinia";
import "bootstrap/dist/css/bootstrap.min.css";

import Modal from "./plugins/modal";

import App from "./App.vue";
import router from "./route";
import { useAuthStore } from "./stores/auth";
import ApiService from "./commons/api.service";

ApiService.init();

const app = createApp(App);
var pinia = createPinia();
app.use(pinia);
app.use(router);
app.use(Modal);

const authStore = useAuthStore();

app.config.globalProperties.$filters = {
  field(value, fieldname) {
    if (value) return value[fieldname];
    else return "";
  },
};

authStore.checkAuth().finally(() => {
  app.mount("#app");
});
