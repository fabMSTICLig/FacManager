import { defineStore } from "pinia";
import { ref } from "vue";
import useCRUDStore from "./useCRUDStore";
import ApiService from "@/commons/api.service";

export const useManagersStore = defineStore("managers", () => {

  const events = ref(null);
  async function fetchEvents(params = {}) {
    const { data } = await ApiService.query("managers/events", params);
    events.value=data;
    return data;
  }
  return {...useCRUDStore("managers"), events, fetchEvents}
});
