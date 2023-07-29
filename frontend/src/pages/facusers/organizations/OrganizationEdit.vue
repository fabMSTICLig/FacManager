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
            Organizations: <strong>{{ cardName }}</strong>
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
            <div class="col-12">
              <label class="form-label" for="contact">Contact</label>
              <input
                id="contact"
                v-model="object.contact"
                class="form-control"
                type="email"
              />
            </div>

            <div class="col-12">
              <label class="form-label" for="type">Type</label>
              <select id="type" v-model="object.type" class="form-select">
                <option
                  v-for="(typename, type) in types"
                  :key="type"
                  :value="type"
                  v-text="typename"
                />
              </select>
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
import { useOrganizationsStore } from "@/stores/organizations";

const store = useOrganizationsStore();
const { types } = storeToRefs(store);
const {
  editorForm,
  object,
  isNew,
  initObject,
  create,
  update,
  destroy,
  cancel,
} = useEditor(store, { name: "", type: null }, { name: "organizations" });

const cardName = computed(() =>
  isNew.value ? "New organization" : object.value.name
);
const route = useRoute();

onBeforeMount(async () => {
  await store.fetchTypes();
  await initObject(route);
});
</script>
