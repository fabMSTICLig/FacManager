import { defineStore } from "pinia";
import useCRUDStore from "./useCRUDStore";

export const useReservationTypesStore = defineStore("reservation_types", () => {
  return useCRUDStore("reservation_types")
});
export const useReservationsStore = defineStore("reservations", () => {
  return useCRUDStore("reservations")
});
