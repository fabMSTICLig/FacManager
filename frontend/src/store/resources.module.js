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
