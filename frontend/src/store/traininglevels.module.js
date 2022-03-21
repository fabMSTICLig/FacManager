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
