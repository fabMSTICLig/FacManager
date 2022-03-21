import createCrud from "./crud.factory";
import ApiService from "@/common/api.service";

const supplies_extra = {
  state: {
    units: [],
  },
  getters: {
    units(state) {
      return state.units;
    },
  },
  actions: {
    async fetchUnits({ commit }) {
      const { data } = await ApiService.query("supplies/units", {});
      commit("setUnits", data);
      return data;
    },
  },
  mutations: {
    setUnits(state, supply_units) {
      state.units = supply_units;
    },
  },
};
export const supplies = createCrud("supplies", supplies_extra);
export const supply_usages = createCrud("supply_usages", {});
