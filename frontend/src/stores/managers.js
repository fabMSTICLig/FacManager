import { defineStore } from "pinia";
import { ref } from "vue";
import useCRUDStore from "./useCRUDStore";
import ApiService from "@/commons/api.service";

export const useManagersStore = defineStore("managers", () => {
  const { objects, count, list, getById, fetchSingle } =
    useCRUDStore("managers");

  async function fetchList(params = {}, prefix = "") {
    const { data } = await ApiService.query(prefix + resource, params);
    setData(data);
    return data.results;
  }

  function setData(data) {
    objects.value = {};
    data.results.forEach((m) => {
      objects.value[m["id"].toString()] = {
        id: m["id"],
        user: m["user"],
        name: m["name"],
        businessHours: m["business_hours"].map((slot) => {
          return {
            daysOfWeek: slot["days_of_week"],
            startTime: slot["start_time"],
            endTime: slot["end_time"],
          };
        }),
      };
    });
    count.value = data.count;
  }
  return {
    objects,
    count,
    list,
    getById,
    fetchList,
    fetchSingle,
    setData,
  };
});
