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
        <div class="card-header">
          <h3>{{ cardName }}</h3>
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
                    type="text"
                    required
                  />
                </div>
                <div class="mb-3">
                  <label class="form-label" for="description">Description</label
                  ><textarea
                    id="description"
                    v-model="object.description"
                    rows="5"
                    class="form-control"
                  />
                </div>
                <div class="mb-3 form-check form-switch">
                  <input
                    id="check-active"
                    v-model="object.need_manager"
                    type="checkbox"
                    class="form-check-input"
                  />
                  <label class="form-check-label" for="check-active"
                    >Need Manager</label
                  >
                </div>
                <div class="col-12">
                  <label class="form-label" for="minTimeSlot"
                    >Min Time Slot</label
                  >
                  <input
                    id="minTimeSlot"
                    v-model="object.min_time_slot"
                    class="form-control"
                    type="number"
                    step="0.5"
                    required
                  />
                </div>
                <div class="col-12">
                  <label class="form-label" for="maxTimeSlot"
                    >Max Time Slot</label
                  >
                  <input
                    id="maxTimeSlot"
                    v-model="object.max_time_slot"
                    class="form-control"
                    type="number"
                    step="0.5"
                    required
                  />
                </div>
              </fieldset>
            </div>
            <div class="col-12 col-md-6">
              <fieldset>
                <legend>Needs</legend>
                <div class="mb-3">
                  <DynList v-model="object.needs" ressource="machine_models" />
                </div>
              </fieldset>
            </div>

            <div class="btn-group col-auto" role="group">
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
                v-if="!isNew"
                class="btn btn-danger"
                type="button"
                @click.prevent="destroy()"
              >
                Delete
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
import { useStore } from "vuex";
import { useRoute } from "vue-router";

import useEditor from "@/composables/useEditor";
import DynList from "@/components/ui/DynList.vue";

const store = useStore();

const { editorForm, object, isNew, initObject, create, update, destroy } =
  useEditor("reservation_types", { name: "", needs: [], need_manager:false, min_time_slot:1, max_time_slot:2 }, "Reservation Type");

const cardName = computed(() =>
  isNew.value ? "New Reservation type" : object.value.name
);

const route = useRoute();

onBeforeMount(() => {
  return initObject(route);
});
</script>
