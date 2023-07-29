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
            Projects: <strong>{{ cardName }}</strong>
          </h3>
          <div class="col-auto btn-group float-end" role="group">
            <router-link
              v-if="!isNew"
              class="btn btn-primary"
              role="button"
              :to="{
                name: 'projectusages',
                params: { projectid: object.id },
              }"
            >
              Usages
            </router-link>

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
                    type="text"
                    required
                  />
                </div>
                <div class="col-12">
                  <label class="form-label" for="startDate">Start date :</label>
                  <input
                    id="startDate"
                    v-model="object.start_date"
                    class="form-control"
                    type="date"
                    required
                  />
                </div>
                <div class="col-12">
                  <label class="form-label" for="endDate">End date :</label>
                  <input
                    id="endDate"
                    v-model="object.end_date"
                    class="form-control"
                    type="date"
                    required
                  />
                </div>

                <div class="col-12">
                  <label class="form-label" for="description"
                    >Description :</label
                  >
                  <textarea
                    id="descrption"
                    v-model="object.description"
                    class="form-control"
                  />
                </div>
                <div class="col-12">
                  <label class="form-label" for="user">Referent :</label>
                  <Multiselect
                    id="user"
                    ref="msuser"
                    v-model="object.referent"
                    placeholder="Select a user"
                    :filter-results="false"
                    :min-chars="3"
                    :resolve-on-load="false"
                    :delay="1"
                    :searchable="true"
                    :options="findUser"
                  />
                </div>
              </fieldset>
            </div>
            <div class="col-12 col-md-6">
              <fieldset>
                <legend>Members</legend>
                <UserDynList v-model="object.members"> </UserDynList>
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
import { computed, ref, onBeforeMount } from "vue";
import { useRoute } from "vue-router";

import Multiselect from "@vueform/multiselect";
import UserDynList from "@/components/ui/UserDynList.vue";
import useEditor from "@/composables/useEditor";

import { useProjectsStore } from "@/stores/projects";
import { useUsersStore } from "@/stores/users";

const store = useProjectsStore();
const {
  editorForm,
  object,
  isNew,
  initObject,
  create,
  update,
  destroy,
  cancel,
} = useEditor(store, { name: "", members: [] }, { name: "projects" });

const cardName = computed(() =>
  isNew.value ? "New project" : object.value.name
);
const route = useRoute();

const usersStore = useUsersStore();
const msuser = ref();
async function findUser(query) {
  let users = await usersStore.fetchList({ search: query });
  return users.map((u) => {
    return {
      label: "@" + u.username + " " + u.first_name + " " + u.last_name,
      value: u.id,
    };
  });
}

onBeforeMount(async () => {
  await initObject(route);
  if (object.value.referent) {
    let u = await usersStore.fetchSingle(object.value.referent);
    msuser.value.select({
      label: "@" + u.username + " " + u.first_name + " " + u.last_name,
      value: u.id,
    });
  }
});
</script>
<style src="@vueform/multiselect/themes/default.css"></style>
