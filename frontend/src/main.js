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
import "bootstrap/dist/css/bootstrap.min.css";

import Modal from "./plugins/modal";

import App from "./App.vue";
import router from "./route";
import store from "./store";
import ApiService from "./common/api.service";

ApiService.init();

const app = createApp(App).use(store);
app.use(Modal);

app.config.globalProperties.$filters = {
  field(value, fieldname) {
    if (value) return value[fieldname];
    else return "";
  },
};

store.dispatch("checkAuth").catch(()=>{}).finally(() => {
  app.use(router).mount("#app");
});
