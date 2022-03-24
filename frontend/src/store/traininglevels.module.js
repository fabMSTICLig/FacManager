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
import createCrud from "./crud.factory";

const training_levels_extra = {
  actions: {
    async bulkUpdate({ commit, getters }, { userid, tls }) {
      const response = await ApiService.put("users/"+userid+"/training_levels", tls)
      commit("fetchListSuccess", response.data);
      return getters.list;
    }
  },
  mutations: {
      fetchListSuccess(state, data) {
        let entities = {};
        data.forEach((m) => {
          entities[m["machine_model"].toString()] = m;
        });
        state.entities = entities;
      },
      fetchSingleSuccess(state, data) {
        const id = data["machine_model"].toString();
        state.entities = { ...state.entities, [id]: data };
      },
      createSuccess(state, data) {
        if (data) {
          const id = data["machine_model"].toString();
          state.entities = { ...state.entities, [id]: data };
        }
      },
      updateSuccess(state, data) {
        if (data["machine_model"]) {
          const id = data["machine_model"].toString();
          state.entities = { ...state.entities, [id]: data };
        }
      },
      destroySuccess(state, id) {
        delete state.entities[id.toString()];
      },
    },

};

export const training_levels = createCrud("training_levels", training_levels_extra);
export default training_levels;
