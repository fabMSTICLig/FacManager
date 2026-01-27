import { ref } from "vue";
import { defineStore } from "pinia";
import ApiService from "@/commons/api.service";
import useCRUDStore from "./useCRUDStore";

export const useOrganizationsStore = defineStore("organizations", () => {
  const types = ref({});
  async function fetchTypes() {
    const { data } = await ApiService.query("organizations/types");
    types.value = data;
    return data;
  }
  return { ...useCRUDStore("organizations"), types, fetchTypes };
});
