<template>
  <nav class="navbar navbar-light navbar-expand-md">
    <div class="container-fluid">
      <a class="navbar-brand" href="/"
        ><strong>{{ title }}</strong></a
      >
      <button
        data-toggle="collapse"
        class="navbar-toggler"
        data-target="#navcol-1"
        @click="collapse"
      >
        <span class="sr-only">Toggle navigation</span
        ><span class="navbar-toggler-icon" />
      </button>
      <div id="navcol-1" :class="collapsed">
        <ul class="nav navbar-nav me-auto">
          <li class="nav-item" role="presentation">
            <router-link
              active-class="active"
              class="nav-link"
              exact
              :to="{ name: 'home' }"
            >
              Home
            </router-link>
          </li>
          <li v-if="isAuthenticated" class="nav-item" role="presentation">
            <router-link
              active-class="active"
              class="nav-link"
              exact
              :to="{ name: 'reservations' }"
            >
              Reservations
            </router-link>
          </li>
          <Dropdown v-if="isAdmin" :items="usersroutes" label="Users" is-nav />
          <Dropdown v-if="isAdmin" :items="fabroutes" label="Fab" is-nav />
        </ul>
        <ul v-if="isAuthenticated" class="nav navbar-nav d-flex">
          <Dropdown :items="authroutes" :label="authUser.username" is-nav />

          <li class="nav-item" role="presentation">
            <a class="nav-link" href="#" @click.prevent="logout">Logout </a>
          </li>
        </ul>
        <ul v-else class="nav navbar-nav">
          <li class="nav-item" role="presentation">
            <a v-if="cas" class="nav-link" href="/cas/login">CAS</a>
          </li>
          <li class="nav-item" role="presentation">
            <a class="nav-link" href="#" @click.prevent="showLogin = true"
              >Login</a
            >
          </li>
        </ul>
      </div>
    </div>
    <modal
      id="modal-login"
      title="Login"
      :show="showLogin"
      :resolve="() => (showLogin = false)"
      hide-footer
    >
      <form class="form">
        <div class="invalid-feedback d-block" v-if="wrongCredentials">
          Wrong Credentials
        </div>
        <div class="mb-3">
          <label for="username" class="form-label">Username</label>
          <input
            v-model="username"
            type="text"
            class="form-control"
            id="username"
          />
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input
            v-model="password"
            type="password"
            class="form-control"
            id="password"
          />
        </div>
        <button type="button" class="btn btn-primary" @click="login">
          Submit
        </button>
      </form>
    </modal>
  </nav>
</template>

<script setup>
import { ref, computed } from "vue";
import { useStore } from "vuex";
import Modal from "@/plugins/modal";
import Dropdown from "./ui/Dropdown.vue";

const title = import.meta.env.VITE_APP_TITLE;
const cas = import.meta.env.VITE_APP_CASNAME;

const usersroutes = [
  {
    to: { name: "users" },
    label: "Users",
  },
  {
    to: { name: "projects" },
    label: "Projects",
  },
  {
    to: { name: "organizations" },
    label: "Organizations",
  },
];
const fabroutes = [
  {
    to: { name: "supplies" },
    label: "Supplies",
  },
  {
    to: { name: "machines" },
    label: "Machines",
  },
  {
    to: { name: "managers" },
    label: "Managers",
  },
  {
    to: { name: "resatypes" },
    label: "Reservation Types",
  },
  {
    to: { name: "usages" },
    label: "Usages",
  },
];

const authroutes = [
  {
    to: { name: "profile" },
    label: "Profile",
  },
  {
    to: { name: "myusages" },
    label: "My Usages",
  },
];

const collapsed = ref("collapse navbar-collapse");
function collapse() {
  /*
    Emulate bootstrap collapse menu
  */
  if (collapsed.value == "collapse navbar-collapse") {
    collapsed.value = "navbar-collapse";
  } else {
    collapsed.value = "collapse navbar-collapse";
  }
}

const store = useStore();
const authUser = computed(() => store.getters.authUser);
const isAuthenticated = computed(() => store.getters.isAuthenticated);
const isAdmin = computed(() => store.getters.isAdmin);

const showLogin = ref(false);
const wrongCredentials = ref(false);
const username = ref();
const password = ref();

async function login() {
  try {
    const response = await store.dispatch("login", {
      username: username.value,
      password: password.value,
    });
    if (response.status == 202) {
      window.location = "/";
    }
  } catch (e) {
    if (e.response.status == 400) {
      wrongCredentials.value = true;
    }
  }
}

async function logout() {
  if (authUser.value.externe) window.location = "/cas/logout";
  else {
    await store.dispatch("logout");
    window.location = "/";
  }
}
</script>
