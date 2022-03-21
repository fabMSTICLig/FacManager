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
