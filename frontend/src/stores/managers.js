import { defineStore } from "pinia";
import useCRUDStore from "./useCRUDStore";

export const useManagersStore = defineStore("managers", () => {
  return useCRUDStore("managers")
});
