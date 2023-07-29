
import { ref } from "vue";
import { defineStore } from "pinia";
import ApiService from "@/commons/api.service";
import useCRUDStore from "./useCRUDStore";

export const useSuppliesStore = defineStore("supplies", () => {

  const units = ref({});
  async function fetchUnits() {
    const { data } = await ApiService.query("supplies/units");
    units.value = data;
    return data;
  }
  return { ...useCRUDStore("supplies"), units, fetchUnits }
});
export const useSupplyUsagesStore = defineStore("supply_usages", () => {
  return useCRUDStore("supply_usages")
});
