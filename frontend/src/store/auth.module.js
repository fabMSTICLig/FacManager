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

import ApiService from "@/common/api.service";
import axios from "axios";

const state = {
  authUser: {},
  userData: {},
};

const getters = {
  authUser(state) {
    return state.authUser;
  },
  isAuthenticated(state) {
    return !!state.authUser.username;
  },
  isAdmin(state) {
    return state.authUser.is_staff;
  },
  userData(state) {
    return state.userData;
  },
};

const actions = {
  async login(context, infos) {
      return await axios.post("/login/", infos, {baseURL: ""})
  },
  async logout(context) {
      return await axios.get("/logout/", {baseURL: ""})
  },

  async checkAuth(context) {
    try {
      const { data } = await ApiService.query("self", {});
      context.commit("setAuthUser", data.user);
      return data.user;
    } catch (e) {
      context.commit("purgeAuth");
      throw new Error("Not connected");
    }
  },
  async updateAuthUser(context, user) {
    const { data } = await ApiService.update("users", user.id, user);
    context.commit("setAuthUser", data);
    return data;
  },
  async updatePassword(context, passwords) {
    await ApiService.put(`users/${state.authUser.id}/set_password`, passwords);
    return "Password changed";
  },
  async updateRGPD(context) {
    const { data } = await ApiService.post(`self/rgpd`, { accept: true });
    context.state.authUser.rgpd_accept = data["rgpd_accept"];
    context.commit("setAuthUser", context.state.authUser);
  },
  async getUserData(context) {
    try {
      const data = await ApiService.query("self/data", {});
      context.commit("setUserData", data.user);
      return data;
    } catch (e) {
      console.log(e);
      return null;
    }
  },
};

const mutations = {
  setAuthUser(state, user) {
    state.authUser = user;
  },
  purgeAuth(state) {
    state.authUser = {};
  },
  setUserData(state, userData) {
    state.userData = userData;
  },
};

export default {
  state,
  actions,
  mutations,
  getters,
};
