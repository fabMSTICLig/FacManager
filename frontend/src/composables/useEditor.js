import { ref, computed, inject } from "vue";
import { useStore } from "vuex";
import { useRouter, useRoute, onBeforeRouteUpdate } from "vue-router";

export default function useEditor(
  ressource,
  emptyObject,
  objectName,
  {
    prefix = "",
    msgCreated = " created",
    msgUpdated = " updated",
    askDelete = `Do you want to delete this ${objectName} ?`,
  } = {}
) {
  const object = ref(null);
  const editorForm = ref(null);

  const route = useRoute();

  const isNew = computed(() => route.params[route.meta.routeparam] == "new");

  const showModal = inject("show");
  const confirmModal = inject("confirm");

  async function initObject(route) {
    if (route.params[route.meta.routeparam] == "new") {
      object.value = Object.assign({}, emptyObject);
    } else if (parseInt(route.params[route.meta.routeparam], -1) != -1) {
      const data = await store.dispatch(ressource + "/fetchSingle", {
        id: route.params[route.meta.routeparam],
        prefix: prefix,
      });
      object.value = Object.assign({}, data);
    }
    return object.value;
  }

  const store = useStore();
  const router = useRouter();
  async function create() {
    if (editorForm.value.checkValidity()) {
      store
        .dispatch(ressource + "/create", {
          data: object.value,
          prefix: prefix,
        })
        .then((data) => {
          showModal({ content: objectName + msgCreated });
          var params = route.params;
          params[route.meta.routeparam] = data.id;
          router.push({
            name: route.name,
            params: params,
          });
        })
        .catch((error) => {
          console.log(error);
          console.log(JSON.stringify(error));
        });
    } else {
      editorForm.value.reportValidity();
    }
  }
  async function update() {
    if (editorForm.value.checkValidity()) {
      store
        .dispatch(ressource + "/update", {
          id: object.value.id,
          data: object.value,
          prefix: prefix,
        })
        .then((data) => {
          object.value = Object.assign({}, data);
          showModal({ content: objectName + msgUpdated });
        });
    } else {
      editorForm.value.reportValidity();
    }
  }
  async function destroy() {
    const isConfirmed = await confirmModal({
      content: askDelete,
    });
    if (isConfirmed) {
      await store.dispatch(ressource + "/destroy", {
        id: object.value.id,
        prefix: prefix,
      });
      router.push({
        name: route.meta.routedelete,
      });
    }
  }

  onBeforeRouteUpdate(async (to, from, next) => {
    await initObject(to);
    next();
  });

  return {
    editorForm,
    object,
    isNew,
    initObject,
    create,
    update,
    destroy,
  };
}
