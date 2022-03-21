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
