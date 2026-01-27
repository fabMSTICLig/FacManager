<!--
Copyright (C) 2020-2022 LIG Université Grenoble Alpes


This file is part of FacManager.

FacManager is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

FacManager is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with FacManager. If not, see <https://www.gnu.org/licenses/>

@author Germain Lemasson
-->

<template>
  <div class="row">
    <div class="col-12">
      <div
        v-if="object"
        class="card"
      >
        <div class="card-header row justify-content-between">
          <h3 class="col-auto">
            Machines: <strong>{{ cardName }}</strong>
          </h3>
          <div
            class="col-auto btn-group float-end"
            role="group"
          >
            <button
              v-if="!isNew"
              class="btn btn-danger"
              type="button"
              @click.prevent="destroy()"
            >
              Delete
            </button>
          </div>
        </div>
        <div class="card-body">
          <div class="row">
            <div class="col-12 col-md-6">
              <form
                ref="editorForm"
                class="row g-3"
              >
                <fieldset>
                  <legend>Informations</legend>
                  <div class="mb-3">
                    <label
                      class="form-label"
                      for="name"
                    >Name</label><input
                      id="name"
                      v-model="object.name"
                      class="form-control"
                      type="text"
                      required
                    >
                  </div>
                  <div class="mb-3">
                    <label
                      class="form-label"
                      for="description"
                    >Description</label><textarea
                      id="description"
                      v-model="object.description"
                      rows="5"
                      class="form-control"
                    />
                  </div>
                  <div class="mb-3">
                    <label
                      class="form-label"
                      for="diplay"
                    >Display order</label><input
                      id="display"
                      v-model="object.display_order"
                      class="form-control"
                      type="number"
                      min="0"
                      required
                    >
                  </div>
                </fieldset>
              </form>
            </div>
            <div class="col-12 col-md-6">
              <div
                v-if="!isNew"
                class="mb-3"
              >
                <form
                  ref="addForm"
                  class="needs-validation"
                  @submit.prevent="addInstance"
                >
                  <div class="input-group has-validation">
                    <span class="input-group-text">Add</span>
                    <input
                      v-model="newInstanceName"
                      class="form-control"
                      :class="{ 'is-invalid': newInstanceError }"
                      required
                      @input="newInstanceError = false"
                    >
                    <button
                      class="btn btn-primary"
                      type="submit"
                    >
                      Validate
                    </button>
                    <div class="invalid-feedback">
                      An instance already have this name.
                    </div>
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
                      @click.stop="removeInstance(item)"
                    >
                      X
                    </button>
                  </li>
                </ul>
              </div>
              <modal
                id="modal-instance"
                :show="selectedInstance != null"
                :resolve="
                  () => {
                    selectedInstance = null;
                  }
                "
                title="Instance"
                hide-footer
              >
                <form
                  class="row g-3"
                  @submit.prevent="updateInstance"
                >
                  <div class="mb-3">
                    <label
                      class="form-label"
                      for="nameI"
                    >Name</label><input
                      id="nameI"
                      v-model="selectedInstance.name"
                      class="form-control"
                      type="text"
                      required
                    >
                  </div>
                  <div class="col-12">
                    <div
                      class="btn-group float-end"
                      role="group"
                    >
                      <button
                        class="btn btn-primary"
                        type="submit"
                      >
                        Update
                      </button>
                      <button
                        class="btn btn-secondary"
                        type="button"
                        @click.prevent="selectedInstance = null"
                      >
                        Cancel
                      </button>
                    </div>
                  </div>
                </form>
              </modal>
            </div>
            <div class="col-12">
              <div
                class="btn-group"
                role="group"
              >
                <button
                  v-if="isNew"
                  class="btn btn-primary"
                  type="button"
                  @click="create(false)"
                >
                  Add
                </button>
                <button
                  v-if="!isNew"
                  class="btn btn-primary"
                  type="button"
                  @click="update()"
                >
                  Update
                </button>
                <button
                  class="btn btn-secondary"
                  type="button"
                  @click.prevent="cancel()"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, computed, onBeforeMount } from "vue";
import { useRoute } from "vue-router";
import Modal from "@/plugins/modal";
import { useMachineModelsStore } from "@/stores/machines";

import useEditor from "@/composables/useEditor";

const store = useMachineModelsStore();
const {
  editorForm,
  object,
  isNew,
  initObject,
  create,
  update,
  destroy,
  cancel,
} = useEditor(
  store,
  {
    name: "",
    description: "",
    instances: [],
    display_order: 0,
  },
  { name: "machines" },
);

const cardName = computed(() =>
  isNew.value ? "New machine models" : object.value.name,
);
const route = useRoute();

onBeforeMount(async () => {
  await initObject(route);
});
const addForm = ref();
const newInstanceName = ref("");
const newInstanceError = ref(false);
const selectedInstance = ref(null);

function selectInstance(instance) {
  selectedInstance.value = Object.assign({}, instance);
}

async function addInstance() {
  if (addForm.value.checkValidity()) {
    try {
      await store.createInstance({
        name: newInstanceName.value,
        model: object.value.id,
      });
      newInstanceName.value = "";
    } catch (error) {
      if (error.response && error.response.status == 400) {
        newInstanceError.value = true;
      }
    }
  } else {
    addForm.value.reportValidity();
  }
}
async function updateInstance() {
  await store.updateInstance(selectedInstance.value.id, selectedInstance.value);
  selectedInstance.value = null;
}
async function removeInstance(instance) {
  await store.destroyInstance(instance.id, object.value.id);
}
</script>
