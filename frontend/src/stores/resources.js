import { defineStore } from "pinia";
import { ref } from "vue";
import axios from "axios";
import ApiService from "@/commons/api.service";
import { useMachineModelsStore, useMachinesStore } from "@/stores/machines";
import { useManagersStore } from "@/stores/managers";
import { useReservationTypesStore } from "@/stores/reservations";
import { useSuppliesStore } from "@/stores/supplies";

export const useResourcesStore = defineStore("resources", () => {
  const businessHours = ref([]);
  const minHour = ref("08:00");
  const maxHour = ref("20:00");

  async function fetchResources(payload = { min: false }) {
    let response = null;
    try {
      response = await axios.get(
        "/static/resources" + (payload.min ? ".min" : "") + ".json",
        {
          baseURL: "",
        },
      );
    } catch (error) {
      if (error.response.status == 404) {
        response = await ApiService.get("/refresh");
      }
    }
    const data = response.data;

    minHour.value = data["business_hours"]["min_hour"];
    maxHour.value = data["business_hours"]["max_hour"];
    businessHours.value = data["business_hours"]["slots"].map((slot) => {
      return {
        daysOfWeek: slot["days_of_week"],
        startTime: slot["start_time"],
        endTime: slot["end_time"],
      };
    });

    const machineStore = useMachinesStore();
    machineStore.setData({
      results: data["machines"],
      count: data["machines"].length,
    });
    const managersStore = useManagersStore();
    managersStore.setData({
      results: data["managers"],
      count: data["managers"].length,
    });
    if (!payload.min) {
      const reservationTypesStore = useReservationTypesStore();
      reservationTypesStore.setData({
        results: data["reservation_types"],
        count: data["reservation_types"].length,
      });
      const machineModelsStore = useMachineModelsStore();
      machineModelsStore.setData({
        results: data["machine_models"],
        count: data["machine_models"].length,
      });
      const suppliesStore = useSuppliesStore();
      suppliesStore.setData({
        results: data["supplies"],
        count: data["supplies"].length,
      });
    }
    return data;
  }

  return { fetchResources, businessHours, minHour, maxHour };
});
