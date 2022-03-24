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

import createCrud from "./crud.factory";
import ApiService from "@/common/api.service";

const organizations_extra = {
  state: {
    types: [],
  },
  getters: {
    types(state) {
      return state.types;
    },
  },
  actions: {
    async fetchTypes({ commit }) {
      const { data } = await ApiService.query("organizations/types", {});
      commit("setTypes", data);
      return data;
    },
  },
  mutations: {
    setTypes(state, organization_types) {
      state.types = organization_types;
    },
  },
};
const organizations = createCrud("organizations", organizations_extra);
export default organizations;
