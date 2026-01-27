import { ref, computed } from "vue";
import { defineStore } from "pinia";
import ApiService from "@/commons/api.service";

export const useTrainingLevelsStore = defineStore("training_levels", () => {
  const objects = ref({});
  const count = ref(0);

  const list = computed(() => Object.values(objects.value));

  async function bulkUpdate(userid, tls) {
    const { data } = await ApiService.put(
      "users/" + userid + "/training_levels",
      tls,
    );
    objects.value = {};
    data.forEach((m) => {
      objects.value[m["machine_model"].toString()] = m;
    });
    count.value = data.count;

    return data;
  }

  async function fetchList(params = {}, prefix) {
    const { data } = await ApiService.query(prefix + "training_levels", params);
    objects.value = {};
    data.forEach((m) => {
      objects.value[m["machine_model"].toString()] = m;
    });
    count.value = data.count;

    return data;
  }
  async function fetchSingle(machine_model, prefix = "") {
    if (Object.keys(objects.value).indexOf(machine_model) > -1)
      return objects.value[machine_model];

    const { data } = await ApiService.get(
      prefix + "training_levels",
      machine_model,
    );
    objects.value = { ...objects.value, [machine_model]: data };
    return data;
  }
  async function create(dataIn, prefix = "") {
    const { data } = await ApiService.post(prefix + "training_levels", dataIn);
    objects.value = { ...objects.value, [data.machine_model]: data };
    return data;
  }
  async function update(machine_model, dataIn, prefix = "", params) {
    const { data } = await ApiService.update(
      prefix + "training_levels",
      machine_model,
      dataIn,
      params,
    );
    objects.value = { ...objects.value, [machine_model]: data };
    return data;
  }
  async function destroy(machine_model, prefix = "") {
    const { data } = await ApiService.delete(
      prefix + "training_levels",
      machine_model,
    );
    delete objects.value[machine_model.toString()];
    return data;
  }

  return {
    objects,
    count,
    list,
    bulkUpdate,
    fetchList,
    fetchSingle,
    create,
    update,
    destroy,
  };
});
