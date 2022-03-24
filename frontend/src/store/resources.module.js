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
import ApiService from "@/common/api.service";

const resources = {
  namespaced: true,
  actions: {
    async fetchResources({ commit }, payload = { min: false }) {
      let response = null;
      try{
        response = await axios
        .get("/static/resources" + (payload.min ? ".min" : "") + ".json", {
          baseURL: ""
        })
      }
      catch(error){
        if(error.response.status==404)
        {
          response = await ApiService.get("/refresh")
        }

      }
      const data = response.data
      commit("machines/fetchListSuccess", {results:data["machines"], count:data["machines"].length}, { root: true });
      commit("managers/fetchListSuccess", {results:data["managers"], count:data["managers"].length}, { root: true });
      if (!payload.min) {
        commit(
          "reservation_types/fetchListSuccess",
          {results:data["reservation_types"], count:data["reservation_types"].length},{ root: true }
        );
        commit(
          "machine_models/fetchListSuccess",
          {results:data["machine_models"], count:data["machine_models"].length},{ root: true }
        );
        commit("supplies/fetchListSuccess", {results:data["supplies"], count:data["supplies"].length},{ root: true });
      }
      return data;
    }
  }
};

export default resources;
