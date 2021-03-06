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
        <div class="card-header">
          <h3>{{ cardName }}</h3>
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
            <div class="col-12">
              <label
                class="form-label"
                for="contact"
              >Contact</label>
              <input
                id="contact"
                v-model="object.contact"
                class="form-control"
                type="email"
              >
            </div>

            <div class="col-12">
              <label
                class="form-label"
                for="type"
              >Type</label>
              <select
                id="type"
                v-model="object.type"
                class="form-select"
              >
                <option
                  v-for="(typename, type) in organizationTypes"
                  :key="type"
                  :value="type"
                  v-text="typename"
                />
              </select>
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

const store = useStore();

const { editorForm, object, isNew, initObject, create, update, destroy } =
  useEditor("organizations", { name: "", type: null }, "Organization");

const cardName = computed(() =>
  isNew.value ? "Nouvelle organization" : object.value.name
);
const organizationTypes = computed(() => store.getters["organizations/types"]);

const route = useRoute();

onBeforeMount(() => {
  store.dispatch("organizations/fetchTypes").then(() => {
    return initObject(route);
  });
});
</script>
