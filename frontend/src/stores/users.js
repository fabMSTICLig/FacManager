import { defineStore } from "pinia";
import useCRUDStore from "./useCRUDStore";

export const useUsersStore = defineStore("users", () => {
  return useCRUDStore("users")
});
