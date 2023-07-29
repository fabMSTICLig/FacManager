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
      <div v-if="object" class="card">
        <div class="card-header row justify-content-between">
          <h3 class="col-auto">
            Supplies: <strong>{{ cardName }}</strong>
          </h3>
          <div class="col-auto btn-group float-end" role="group">
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
          <form ref="editorForm" class="row g-3">
            <div class="col-12 col-md-6">
              <fieldset>
                <legend>Informations</legend>
                <div class="col-12">
                  <label class="form-label" for="name">Name</label>
                  <input
                    id="name"
                    v-model="object.name"
                    class="form-control"
                    unit="text"
                    required
                  />
                </div>
                <div class="col-12">
                  <label class="form-label" for="description"
                    >Description :</label
                  >
                  <textarea
                    id="description"
                    v-model="object.description"
                    class="form-control"
                  />
                </div>

                <div class="col-12">
                  <label class="form-label" for="unit">Unit</label>
                  <select id="unit" v-model="object.unit" class="form-select">
                    <option
                      v-for="(unitname, unit) in units"
                      :key="unit"
                      :value="parseInt(unit)"
                      v-text="unitname"
                    />
                  </select>
                </div>
              </fieldset>
            </div>
            <div class="col-12 col-md-6">
              <fieldset>
                <legend>Machine models</legend>
                <div class="mb-3">
                  <DynList v-model="object.models" :resource="fetchMachineModels" />
                </div>
              </fieldset>
            </div>

            <div class="btn-group col-auto" role="group">
              <button
                v-if="isNew"
                class="btn btn-primary"
                unit="button"
                @click.prevent="create()"
              >
                Add
              </button>
              <button
                v-if="!isNew"
                class="btn btn-primary"
                unit="button"
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
import DynList from "@/components/ui/DynList.vue";
import { useSuppliesStore } from "@/stores/supplies";
import { useMachineModelsStore } from "@/stores/machines";

const store = useSuppliesStore();
const { units } = storeToRefs(store);
const mmstore = useMachineModelsStore();
const { fetchList:fetchMachineModels } = mmstore;
const {
  editorForm,
  object,
  isNew,
  initObject,
  create,
  update,
  destroy,
  cancel,
} = useEditor(store, { name: "", models:[] , units: null }, { name: "supplies" });

const cardName = computed(() =>
  isNew.value ? "New supply" : object.value.name
);
const route = useRoute();

onBeforeMount(async () => {
  await store.fetchUnits();
  await initObject(route);
});
</script>
