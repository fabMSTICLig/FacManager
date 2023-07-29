import { defineStore } from "pinia";
import useCRUDStore from "./useCRUDStore";

export const useProjectsStore = defineStore("projects", () => {
  return useCRUDStore("projects")
});
