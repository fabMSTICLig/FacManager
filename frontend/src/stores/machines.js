import { defineStore } from "pinia";
import useCRUDStore from "./useCRUDStore";
import ApiService from "@/commons/api.service";

export const useMachinesStore = defineStore("machines", () => {
  return useCRUDStore("machines");
});
export const useMachineModelsStore = defineStore("machine_models", () => {
  const {
    objects,
    count,
    list,
    getById,
    fetchList,
    fetchSingle,
    setData,
    create,
    update,
    destroy,
  } = useCRUDStore("machine_models");
  async function createInstance(dataI) {
    const { data } = await ApiService.post("machines", dataI);
    const model = data["model"].toString();
    objects.value[model].instances.push(data);
    return data;
  }
  async function updateInstance(id, dataI) {
    const { data } = await ApiService.update("machines", id, dataI);
    if (data["id"]) {
      const model = data["model"].toString();
      const listIndex = objects.value[model].instances.findIndex(
        (e) => e.id == data["id"],
      );
      if (listIndex >= 0) {
        objects.value[model].instances.splice(listIndex, 1, data);
      }
    }
    return data;
  }
  async function destroyInstance(id, model) {
    const { data } = await ApiService.delete("machines", id);
    const listIndex = objects.value[model.toString()].instances.findIndex(
      (e) => e.id == id,
    );
    if (listIndex >= 0) {
      objects.value[model.toString()].instances.splice(listIndex, 1);
    }
    return data;
  }
  return {
    objects,
    count,
    list,
    getById,
    fetchList,
    fetchSingle,
    setData,
    create,
    update,
    destroy,
    createInstance,
    updateInstance,
    destroyInstance,
  };
});
