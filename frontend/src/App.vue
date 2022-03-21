<template>
  <div class="container-fluid">
    <div v-if="loaded">
      <Header />
      <router-view class="mr-5 ml-5" />
      <Footer />
    </div>
    <modal
      id="modal-cookie"
      title="Utilisation de cookie"
      :show="showCookie"
      hide-footer
    >
      <p>
        Ce site utilise des cookies afin de fonctionner. Ils sont uniquement
        utilisés pour gerer la session de l'utilisateur. Il n'y a pas de cookie
        de tierces parties ou d'utilisation à des fins statistiques.
      </p>

      <div>
        <div class="btn-group" role="group" aria-label="Accepter">
          <button type="button" class="btn btn-primary" @click="validCookie">
            J'ai compris
          </button>
        </div>
      </div>
    </modal>
  </div>
  <svg style="display: none" version="2.0">
    <defs>
      <symbol id="check" viewBox="0 0 20 20">
        <path
          fill="#28a745"
          d="M9.917,0.875c-5.086,0-9.208,4.123-9.208,9.208c0,5.086,4.123,9.208,9.208,9.208s9.208-4.122,9.208-9.208
								C19.125,4.998,15.003,0.875,9.917,0.875z M9.917,18.141c-4.451,0-8.058-3.607-8.058-8.058s3.607-8.057,8.058-8.057
								c4.449,0,8.057,3.607,8.057,8.057S14.366,18.141,9.917,18.141z M13.851,6.794l-5.373,5.372L5.984,9.672
								c-0.219-0.219-0.575-0.219-0.795,0c-0.219,0.22-0.219,0.575,0,0.794l2.823,2.823c0.02,0.028,0.031,0.059,0.055,0.083
								c0.113,0.113,0.263,0.166,0.411,0.162c0.148,0.004,0.298-0.049,0.411-0.162c0.024-0.024,0.036-0.055,0.055-0.083l5.701-5.7
                c0.219-0.219,0.219-0.575,0-0.794C14.425,6.575,14.069,6.575,13.851,6.794z"
        ></path>
      </symbol>
      <symbol id="cross" viewBox="0 0 20 20">
        <path
          fill="#dc3545"
          d="M13.864,6.136c-0.22-0.219-0.576-0.219-0.795,0L10,9.206l-3.07-3.07c-0.219-0.219-0.575-0.219-0.795,0
								c-0.219,0.22-0.219,0.576,0,0.795L9.205,10l-3.07,3.07c-0.219,0.219-0.219,0.574,0,0.794c0.22,0.22,0.576,0.22,0.795,0L10,10.795
								l3.069,3.069c0.219,0.22,0.575,0.22,0.795,0c0.219-0.22,0.219-0.575,0-0.794L10.794,10l3.07-3.07
								C14.083,6.711,14.083,6.355,13.864,6.136z M10,0.792c-5.086,0-9.208,4.123-9.208,9.208c0,5.085,4.123,9.208,9.208,9.208
								s9.208-4.122,9.208-9.208C19.208,4.915,15.086,0.792,10,0.792z M10,18.058c-4.451,0-8.057-3.607-8.057-8.057
                c0-4.451,3.606-8.057,8.057-8.057c4.449,0,8.058,3.606,8.058,8.057C18.058,14.45,14.449,18.058,10,18.058z"
        ></path>
      </symbol>
      <symbol id="delete" viewBox="0 0 20 20">
        <path
          d="M17.114,3.923h-4.589V2.427c0-0.252-0.207-0.459-0.46-0.459H7.935c-0.252,0-0.459,0.207-0.459,0.459v1.496h-4.59c-0.252,0-0.459,0.205-0.459,0.459c0,0.252,0.207,0.459,0.459,0.459h1.51v12.732c0,0.252,0.207,0.459,0.459,0.459h10.29c0.254,0,0.459-0.207,0.459-0.459V4.841h1.511c0.252,0,0.459-0.207,0.459-0.459C17.573,4.127,17.366,3.923,17.114,3.923M8.394,2.886h3.214v0.918H8.394V2.886z M14.686,17.114H5.314V4.841h9.372V17.114z M12.525,7.306v7.344c0,0.252-0.207,0.459-0.46,0.459s-0.458-0.207-0.458-0.459V7.306c0-0.254,0.205-0.459,0.458-0.459S12.525,7.051,12.525,7.306M8.394,7.306v7.344c0,0.252-0.207,0.459-0.459,0.459s-0.459-0.207-0.459-0.459V7.306c0-0.254,0.207-0.459,0.459-0.459S8.394,7.051,8.394,7.306"
        ></path>
      </symbol>
      <symbol id="update" viewBox="0 0 20 20">
        <path
          d="M3.254,6.572c0.008,0.072,0.048,0.123,0.082,0.187c0.036,0.07,0.06,0.137,0.12,0.187C3.47,6.957,3.47,6.978,3.484,6.988c0.048,0.034,0.108,0.018,0.162,0.035c0.057,0.019,0.1,0.066,0.164,0.066c0.004,0,0.01,0,0.015,0l2.934-0.074c0.317-0.007,0.568-0.271,0.56-0.589C7.311,6.113,7.055,5.865,6.744,5.865c-0.005,0-0.01,0-0.015,0L5.074,5.907c2.146-2.118,5.604-2.634,7.971-1.007c2.775,1.912,3.48,5.726,1.57,8.501c-1.912,2.781-5.729,3.486-8.507,1.572c-0.259-0.18-0.618-0.119-0.799,0.146c-0.18,0.262-0.114,0.621,0.148,0.801c1.254,0.863,2.687,1.279,4.106,1.279c2.313,0,4.591-1.1,6.001-3.146c2.268-3.297,1.432-7.829-1.867-10.101c-2.781-1.913-6.816-1.36-9.351,1.058L4.309,3.567C4.303,3.252,4.036,3.069,3.72,3.007C3.402,3.015,3.151,3.279,3.16,3.597l0.075,2.932C3.234,6.547,3.251,6.556,3.254,6.572z"
        ></path>
      </symbol>
    </defs>
  </svg>
</template>

<script setup>
import { useStore } from "vuex";
import Modal from "@/plugins/modal";
import Header from "@/components/AppHeader.vue";
import Footer from "@/components/AppFooter.vue";

import { ref, onMounted } from "vue";

const loaded = ref(false);
const showCookie = ref(false);
const store = useStore();
onMounted(async () => {
  document.title = import.meta.env.VITE_APP_TITLE;
  try {
    if (store.getters.isAuthenticated) {
      console.log("connected");
      const usersPromise = import("./store/users.module");
      const organizationsPromise = import("./store/organizations.module");
      const suppliesPromise = import("./store/supplies.module");
      const projectsPromise = import("./store/projects.module");
      const machinesPromise = import("./store/machines.module");
      const availabilitiesPromise = import("./store/availabilities.module");
      const trainingLevelsPromise = import("./store/traininglevels.module");

      const users = await usersPromise;
      const organizations = await organizationsPromise;
      const supplies = await suppliesPromise;
      const projects = await projectsPromise;
      const machines = await machinesPromise;
      const availabilities = await availabilitiesPromise;
      const trainingLevels = await trainingLevelsPromise;

      store.registerModule("users", users.default);
      store.registerModule("organizations", organizations.default);
      store.registerModule("projects", projects.default);
      store.registerModule("availabilities", availabilities.default);
      store.registerModule("training_levels", trainingLevels.default);

      store.registerModule("supplies", supplies.supplies);
      store.registerModule("supply_usages", supplies.supply_usages);

      store.registerModule("machine_models", machines.machine_models);

      await store.dispatch("training_levels/fetchList", {
        prefix: "/users/" + store.getters.authUser.id + "/",
      });
    }
  } catch (e) {
    console.log(e);
  } finally {
    loaded.value = true;
  }

  if (localStorage.getItem("cookiepopup") == null) {
    showCookie.value = true;
  }
});
function validCookie() {
  localStorage.setItem("cookiepopup", "true");
  showCookie.value = false;
}
</script>
<style>
/* -----
SVG Icons - svgicons.sparkk.fr
----- */

.svg-icon {
  width: 2em;
  height: 2em;
}
.svg-icon-small {
  width: 1em;
  height: 1em;
}

</style>
