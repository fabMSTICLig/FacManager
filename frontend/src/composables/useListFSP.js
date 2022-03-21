import { ref, computed, watch } from "vue";
import { useStore } from "vuex";
import useDebouncedRef from "./useDebouncedRef";

export default function useListFSP(
  ressource,
  { fetchParams = ref(), prefix = "", postFetch = null } = {}
) {
  const selectedObject = ref(null);
  const searchInput = useDebouncedRef("");
  const currentPage = ref(1);

  const store = useStore();

  function fetchList() {
    let paramsDefault = {};
    if (searchInput.value) {
      paramsDefault["search"] = searchInput.value;
    }
    paramsDefault.limit = import.meta.env.VITE_APP_MAXLIST;
    paramsDefault.offset =
      (currentPage.value - 1) * import.meta.env.VITE_APP_MAXLIST;
    const ret = store
      .dispatch(ressource + "/fetchList", {
        prefix: prefix,
        params: { ...paramsDefault, ...fetchParams.value },
      })
      .then((list) => {
        let obj = null;
        if (sessionStorage.getItem(ressource + "_object")) {
          let id = parseInt(sessionStorage.getItem(ressource + "_object"));
          obj = list.find((o) => o.id == id);
        }
        if (obj) selectedObject.value = obj;
        else selectedObject.value = list[0];
        return list;
      });
    if (postFetch) return ret.then(postFetch);
    else return ret;
  }

  watch(searchInput, () => {
    currentPage.value = 1;
    fetchList();
  });

  watch(selectedObject, () => {
    if (selectedObject.value)
      sessionStorage.setItem(
        ressource + "_object",
        "" + selectedObject.value.id
      );
    else sessionStorage.removeItem(ressource + "_object");
  });

  const objectsList = computed(() => {
    return store.getters[ressource + "/list"];
  });
  const objectsCount = computed(() => {
    return store.state[ressource].count;
  });

  const pagesCount = computed(() => {
    return Math.ceil(objectsCount.value / import.meta.env.VITE_APP_MAXLIST);
  });
  const perPage = computed(() => {
    return parseInt(import.meta.env.VITE_APP_MAXLIST);
  });

  function onPageChange(page) {
    currentPage.value = page;
    sessionStorage.setItem(ressource + "_page", page);
    fetchList();
  }

  function loadPage() {
    if (sessionStorage.getItem(ressource + "_page")) {
      currentPage.value = parseInt(sessionStorage.getItem(ressource + "_page"));
    }
  }

  return {
    selectedObject,
    searchInput,
    currentPage,
    pagesCount,
    perPage,
    onPageChange,
    loadPage,
    objectsList,
    objectsCount,
    fetchList,
  };
}
