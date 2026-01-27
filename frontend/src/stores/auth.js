import { ref, computed } from "vue";
import { defineStore } from "pinia";
import ApiService from "@/commons/api.service";
import axios from "axios";

export const useAuthStore = defineStore("auth", () => {
  const authUser = ref(null);
  const firstCheck = ref(false);
  let resolveFC = null;
  let pfc = new Promise(function (resolve) {
    resolveFC = resolve;
  });

  const isAuthenticated = computed(() => authUser.value != null);
  const isAdmin = computed(
    () => authUser.value && authUser.value.is_staff == true,
  );
  const isManager = computed(
    () => authUser.value && authUser.value.entities.length != 0,
  );
  async function waitFirstCheck() {
    await pfc;
  }

  async function login(username, password) {
    return await axios.post("/login/", { username, password }, { baseURL: "" });
  }
  async function logout() {
    return await axios.get("/logout/", { baseURL: "" });
  }

  async function checkAuth() {
    try {
      const { data: datauser } = await ApiService.get("self");
      authUser.value = datauser.user;
    } catch (_) {
      authUser.value = null;
    }
    if (!firstCheck.value) {
      firstCheck.value = true;
      resolveFC();
    }
  }

  async function updateUser(user) {
    const { data: datauser } = await ApiService.update("users", user.id, user);
    authUser.value = datauser;
  }
  async function updatePassword(passwords) {
    await ApiService.put(`users/${authUser.value.id}/set_password`, passwords);
    return "Password changed";
  }
  async function updateRGPD() {
    const { data } = await ApiService.post(`self/rgpd`, { accept: true });
    authUser.value.rgpd_accept = data["rgpd_accept"];
  }

  return {
    firstCheck,
    waitFirstCheck,
    login,
    logout,
    authUser,
    isAuthenticated,
    isAdmin,
    isManager,
    checkAuth,
    updateUser,
    updatePassword,
    updateRGPD,
  };
});
