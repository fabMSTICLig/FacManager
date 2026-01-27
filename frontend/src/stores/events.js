import { defineStore } from "pinia";
import useCRUDStore from "./useCRUDStore";

export const useEventsStore = defineStore("events", () => {
  return useCRUDStore("events");
});
