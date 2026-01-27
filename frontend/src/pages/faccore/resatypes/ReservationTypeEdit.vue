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
            Reservation Types: <strong>{{ cardName }}</strong>
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
          <form
            ref="editorForm"
            class="row g-3"
          >
            <div class="col-12">
              <label
                class="form-label"
                for="name"
              >Name</label>
              <input
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
              <label for="machine">Machine model:</label>
              <div class="input-group">
                <select
                  id="machine"
                  v-model="object.machine_model"
                  class="form-control"
                >
                  <option :value="null">
                    None
                  </option>
                  <option
                    v-for="machine in machine_models"
                    :key="machine.id"
                    :value="machine.id"
                  >
                    {{ machine.name }}
                  </option>
                </select>
              </div>
            </div>
            <div class="mb-3 form-check form-switch">
              <input
                id="check-active"
                v-model="object.need_manager"
                type="checkbox"
                class="form-check-input"
              >
              <label
                class="form-check-label"
                for="check-active"
              >Need Manager</label>
            </div>
            <div class="mb-3">
              <label for="speman">Specific Manager:</label>
              <div class="input-group">
                <select
                  id="speman"
                  v-model="object.spe_manager"
                  class="form-control"
                >
                  <option :value="null">
                    None
                  </option>
                  <option
                    v-for="man in managers"
                    :key="man.id"
                    :value="man.id"
                  >
                    {{ man.name }}
                  </option>
                </select>
              </div>
            </div>
            <div
              class="btn-group col-auto"
              role="group"
            >
              <button
                v-if="isNew"
                class="btn btn-primary"
                type="button"
                @click.prevent="create()"
              >
                Add
              </button>
              <button
                v-if="!isNew"
                class="btn btn-primary"
                type="button"
                @click.prevent="update()"
              >
                Update
              </button>
              <button
                class="btn btn-secondary"
                type="button"
                @click.prevent="cancel"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onBeforeMount } from "vue";
import { useRoute } from "vue-router";
import { storeToRefs } from "pinia";

import useEditor from "@/composables/useEditor";
import { useReservationTypesStore } from "@/stores/reservations";
import { useMachineModelsStore } from "@/stores/machines";
import { useManagersStore } from "@/stores/managers";

const mmstore = useMachineModelsStore();
const { objects: machine_models } = storeToRefs(mmstore);
const managersStore = useManagersStore();
const { objects: managers } = storeToRefs(managersStore);

const store = useReservationTypesStore();
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
    need_manager: false,
  },
  { name: "resatypes" },
);

const cardName = computed(() =>
  isNew.value ? "New reservation type" : object.value.name,
);
const route = useRoute();

onBeforeMount(async () => {
  await mmstore.fetchList();
  await managersStore.fetchList();
  await initObject(route);
});
</script>
