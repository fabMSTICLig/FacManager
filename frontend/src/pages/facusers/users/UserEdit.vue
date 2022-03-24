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
          <h3 class="float-start">{{ cardName }}</h3>
          <div class="btn-group float-end" role="group">
            <router-link
              class="btn btn-primary"
              role="button"
              :to="{
                name: 'userusages',
                params: { userid: object.id },
              }"
            >
              Usages
            </router-link></div>
        </div>
        <div class="card-body">
          <form ref="editorForm" class="row g-3">
            <div class="col-12 col-md-3">
              <fieldset>
                <legend>Informations</legend>
                <div class="mb-3">
                  <label class="form-label">Username</label
                  ><input
                    v-model="object.username"
                    class="form-control"
                    type="text"
                    required
                  />
                </div>
                <div class="mb-3">
                  <label class="form-label">First name</label
                  ><input
                    v-model="object.first_name"
                    class="form-control"
                    type="text"
                    required
                  />
                </div>
                <div class="mb-3">
                  <label class="form-label">Last name</label
                  ><input
                    v-model="object.last_name"
                    class="form-control"
                    type="text"
                    required
                  />
                </div>
                <div class="mb-3">
                  <label class="form-label">Email</label
                  ><input
                    v-model="object.email"
                    class="form-control"
                    type="email"
                    required
                  />
                </div>
                <div class="mb-3 form-check form-switch">
                  <label class="form-check-label" for="check-active"
                    >Charter</label
                  >
                  <input
                    id="check-active"
                    v-model="object.charter"
                    type="checkbox"
                    class="form-check-input"
                  />
                </div>
                <div class="mb-3">
                  <label class="form-label">RGPD accept date</label
                  ><input
                    v-model="object.rgpd_accept"
                    class="form-control"
                    type="date"
                    readonly
                  />
                </div>
              </fieldset>
            </div>
            <div class="col-12 col-md-9">
              <div class="row">
                <div class="col-12 col-md">
                  <fieldset>
                    <legend>Organizations</legend>
                    <div class="mb-3">
                      <DynList
                        v-model="object.organizations"
                        ressource="organizations"
                      />
                    </div>
                  </fieldset>
                </div>
                <div class="col-12 col-md">
                  <fieldset>
                    <legend>Projects</legend>
                    <div class="mb-3">
                      <DynList v-model="object.projects" ressource="projects" />
                    </div>
                  </fieldset>
                </div>
                <div class="col-12 col-md" v-if="object.id">
                  <fieldset>
                    <legend>
                      Training Levels
                      <button
                        @click="updateTLs"
                        type="button"
                        class="btn btn-primary float-end"
                      >
                        Update Training Levels
                      </button>
                    </legend>
                    <table class="table">
                      <tr>
                        <th>Machine Model</th>
                        <th>Level</th>
                        <th>Need Manager</th>
                      </tr>
                      <tr
                        v-for="tl in userTrainingLevels"
                        :key="tl.machine_model"
                      >
                        <td>
                          {{ machineModelName(tl.machine_model) }}
                        </td>
                        <td>
                          <input
                            v-model="tl.level"
                            type="number"
                            class="form-control"
                          />
                        </td>
                        <td>
                          <div>
                            <div class="form-check form-switch">
                              <input
                                type="checkbox"
                                class="form-check-input"
                                v-model="tl.need_manager"
                                :id="'cslevel' + tl.machine_model"
                              />
                            </div>
                          </div>
                        </td>
                      </tr>
                    </table>
                  </fieldset>
                </div>
              </div>
            </div>

            <div class="row">
              <div class="btn-group col-auto" role="group">
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
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onBeforeMount } from "vue";
import { useRoute } from "vue-router";
import { useStore } from "vuex";

import useEditor from "@/composables/useEditor";

import DynList from "@/components/ui/DynList.vue";

const store = useStore();
const { editorForm, object, isNew, initObject, create, update, destroy } =
  useEditor(
    "users",
    {
      username: "",
      first_name: "",
      last_name: "",
      email: "",
      organizations: [],
      projects: [],
    },
    "User"
  );

const cardName = computed(() =>
  isNew.value ? "Nouvel Utilisateur" : object.value.username
);

const userTrainingLevels = ref([]);
function machineModelName(id) {
  let mm = store.getters["machine_models/byId"](id);
  if (mm) return mm.name;
  else return "";
}

function updateTLs() {
  store.dispatch("training_levels/bulkUpdate", {
    tls: userTrainingLevels.value,
    userid: object.value.id,
  });
}

const route = useRoute();

onBeforeMount(async () => {
  await initObject(route);

  if (object.value.id) {
    const data = await store.dispatch("training_levels/fetchList", {
      prefix: "/users/" + object.value.id + "/",
    });

    userTrainingLevels.value = data;
  }
});
</script>
