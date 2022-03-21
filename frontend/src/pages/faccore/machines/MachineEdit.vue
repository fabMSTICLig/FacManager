<template>
  <div class="row">
    <div class="col-12">
      <div v-if="object" class="card">
        <div class="card-header">
          <h3 v-text="cardName" />
        </div>
        <div class="card-body">
          <div class="row">
            <div class="col-12 col-md-4">
              <form ref="editorForm" class="row g-3">
                <fieldset>
                  <legend>Informations</legend>
                  <div class="mb-3">
                    <label class="form-label" for="name">Name</label
                    ><input
                      id="name"
                      v-model="object.name"
                      class="form-control"
                      type="text"
                      required
                    />
                  </div>
                  <div class="mb-3">
                    <label class="form-label" for="description"
                      >Description</label
                    ><textarea
                      id="description"
                      v-model="object.description"
                      rows="5"
                      class="form-control"
                    />
                    </div>
                    <div class="mb-3">
                    <label class="form-label" for="diplay">Display order</label
                    ><input
                      id="display"
                      v-model="object.display_order"
                      class="form-control"
                      type="number"
                      min="0"
                      required
                    />
                  </div>

                </fieldset>
              </form>
              <div class="btn-group" role="group">
                <button
                  v-if="isNew"
                  class="btn btn-primary"
                  type="button"
                  @click="create"
                >
                  Add
                </button>
                <button
                  v-if="!isNew"
                  class="btn btn-primary"
                  type="button"
                  @click="update(msg)"
                >
                  Update
                </button>
                <button
                  v-if="!isNew"
                  class="btn btn-danger"
                  type="button"
                  @click="destroy"
                >
                  Delete
                </button>
              </div>
            </div>
            <div class="col-12 col-md-8">
              <div class="row">
                <div class="col-12 col-md-6">
                  <fieldset>
                    <legend>Instances</legend>
                    <form ref="editorInstances" @submit.prevent="addInstance">
                      <div class="input-group">
                        <span class="input-group-text">Add</span>
                        <input
                          v-model="newInstanceName"
                          class="form-control"
                          required
                        />
                        <button class="btn btn-primary" type="submit">
                          Valider
                        </button>
                      </div>
                    </form>
                    <ul class="list-group">
                      <li
                        v-for="item in object.instances"
                        :key="item.id"
                        class="list-group-item list-group-item-action d-flex justify-content-between align-items-center"
                        :class="{
                          active:
                            selectedInstance && item.id == selectedInstance.id,
                        }"
                        @click="selectInstance(item)"
                      >
                        <span>
                          {{ item.name }}
                        </span>
                        <button
                          class="btn btn-danger"
                          type="button"
                          @click.prevent="removeInstance(item)"
                        >
                          X
                        </button>
                      </li>
                    </ul>
                  </fieldset>
                </div>
                <div class="col-12 col-md-6">
                  <div v-if="!isNew && selectedInstance">
                    <form class="row g-3" @submit.prevent="updateInstance">
                      <fieldset>
                        <legend>Instance</legend>
                        <div class="mb-3">
                          <label class="form-label" for="nameI">Name</label
                          ><input
                            id="nameI"
                            v-model="selectedInstance.name"
                            class="form-control"
                            type="text"
                            required
                          />
                        </div>
                      </fieldset>
                      <div class="row">
                        <div class="btn-group col-auto" role="group">
                          <button class="btn btn-primary" type="submit">
                            Update
                          </button>
                        </div>
                      </div>
                    </form>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, computed, inject, onBeforeMount } from "vue";
import { useStore } from "vuex";
import { useRoute } from "vue-router";

import useEditor from "@/composables/useEditor";

const store = useStore();
const route = useRoute();
const showModal = inject("show");

const { editorForm, object, isNew, initObject, create, update, destroy } =
  useEditor(
    "machine_models",
    {
      name: "",
      description: "",
      instances: [],
    },
    "Machine Models"
  );

const cardName = computed(() =>
  isNew.value ? "New Machine Models" : object.value.name
);

const newInstanceName = ref("");
const selectedInstance = ref(null);

function selectInstance(instance) {
  selectedInstance.value = Object.assign({}, instance);
}

async function addInstance() {
  const instance = await store.dispatch("machines/create", {
    data: {
      name: newInstanceName.value,
      model: object.value.id,
    },
  });
  newInstanceName.value = "";
  selectInstance(instance);
  object.value.instances.push(instance);
  showModal({ content: "Instance crée" });
}
async function updateInstance() {
  const instance = await store.dispatch("machines/update", {
    id: selectedInstance.value.id,
    data: selectedInstance.value,
  });
  selectInstance(instance);
  object.value.instances[
    object.value.instances.findIndex((i) => i.id == instance.id)
  ] = instance;
  showModal({ content: "Instance mise à jour" });
}
async function removeInstance(instance) {
  await store.dispatch("machines/destroy", {
    id: instance.id,
  });
  if (instance.id == selectedInstance.value.id) {
    selectedInstance.value = null;
  }
  object.value.instances.splice(
    object.value.instances.findIndex((i) => i.id == instance.id),
    1
  );
  showModal({ content: "Instance supprimée" });
}
onBeforeMount(async () => {
  await initObject(route);
});
</script>
