
import { ref, computed } from "vue";
import ApiService from "@/commons/api.service";

export default function useCRUDStore(resource) {

  const objects = ref({});
  const count = ref(0);

  const list = computed(()=>Object.values(objects.value))


  function getById(id){
    return (id ? objects.value[id.toString()] : null);
  }
  async function fetchList(params = {}, prefix = "") {
    const { data } = await ApiService.query(prefix + resource, params);
    setData(data)
    return data.results;
  }
  function setData(data){
    objects.value={}
    data.results.forEach((m) => {
          objects.value[m["id"].toString()] = m;
        });
    count.value = data.count;
  }
  async function fetchSingle(id, prefix = "" ) {
    if(Object.keys(objects.value).indexOf(id)>-1) return objects.value[id]

    const { data } = await ApiService.get(prefix + resource, id);
    objects.value = { ...objects.value, [id]: data };
    return data;
  }
  async function create(dataIn, prefix = "") {
    const {data} = await ApiService.post(prefix + resource, dataIn);
    objects.value = { ...objects.value, [data.id]: data };
    return data;
  }
  async function update(id, dataIn, prefix = "", params) {
    const {data} = await ApiService.update(prefix + resource, id, dataIn, params);
    objects.value = { ...objects.value, [id]: data };
    return data;
  }
  async function destroy(id, prefix = "") {
    const { data } = await ApiService.delete(prefix + resource, id);
    delete objects.value[id.toString()];
    return data;
  }

  return {objects, count, list, getById, fetchList, fetchSingle, create, update, destroy, setData}
}

