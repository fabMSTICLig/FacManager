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
      <div class="card">
        <div class="card-header">
          <h3 class="float-start">{{ title }}</h3>
          <div class="btn-group float-end" role="group"></div>
        </div>
        <div class="card-body">
          <div class="col-12">
            <h4>Filters</h4>
            <div>
              <form class="row g-3">
                <div class="col-auto">
                  <label for="mindate" class="form-label">Min Date</label>
                  <input
                    type="date"
                    class="form-control"
                    id="mindate"
                    :value="fMinDate"
                  />
                </div>
                <div class="col-auto">
                  <label for="maxdate" class="form-label">Max Date</label>
                  <input
                    type="date"
                    class="form-control"
                    id="maxdate"
                    :value="fMaxDate"
                  />
                </div>
                <div class="col-auto">
                  <label for="status" class="form-label">Status</label>
                  <select class="form-control" id="status" v-model="fStatus">
                    <option></option>
                    <option>Requested</option>
                    <option>Accepted</option>
                    <option>Denied</option>
                    <option>Changed</option>
                  </select>
                </div>
                <div class="col-auto">
                  <label for="type" class="form-label">Type</label>
                  <select class="form-control" id="type" v-model="fType">
                    <option></option>
                    <option v-for="t in resaTypes" :value="t.id">
                      {{ t.name }}
                    </option>
                  </select>
                </div>

                <div class="col-auto">
                  <label for="validated" class="form-label">Validated</label>
                  <select
                    class="form-control"
                    id="validated"
                    v-model="fValidated"
                  >
                    <option></option>
                    <option value="true">True</option>
                    <option value="false">False</option>
                  </select>
                </div>
                <div class="col-auto" v-if="displayUser">
                  <label class="form-label" for="resa-user">User :</label>
                  <Multiselect
                    id="resa-user"
                    ref="msuser"
                    class="form-control"
                    v-model="fUser"
                    placeholder="Select a user"
                    :filter-results="false"
                    :min-chars="3"
                    :resolve-on-load="false"
                    :delay="1"
                    :searchable="true"
                    :options="findUser"
                  />
                </div>
                <div class="col-auto" v-if="displayProject">
                  <label class="form-label" for="project">Project :</label>
                  <Multiselect
                    id="resa-user"
                    ref="msproject"
                    class="form-control"
                    v-model="fProject"
                    placeholder="Select a project"
                    :searchable="true"
                    :options="projectsOptions"
                    valueProp="id"
                    label="name"
                  />
                </div>
                <div class="col-12">
                  <div>
                    <button
                      type="button"
                      class="btn btn-primary"
                      @click="fetchUsages"
                    >
                      Search
                    </button>
                  </div>
                </div>
              </form>
            </div>
          </div>
          <h4>Reservations</h4>
          <table class="table">
            <thead class="table-light">
              <tr>
                <th>Date</th>
                <th>Duration (h)</th>
                <th>Status</th>
                <th v-if="displayUser">User</th>
                <th v-if="displayProject">Project</th>
              </tr>
            </thead>
            <tbody>
              <template v-for="rtype in reservations">
                <tr>
                  <th>{{ rtype.name }}</th>
                  <th>{{ rtype.total }}</th>
                  <th colspan="3"></th>
                </tr>
                <tr v-for="resa in rtype.usages">
                  <td>{{ formatDate(resa.start_date) }}</td>
                  <td>{{ resa.duration }}</td>
                  <td>{{ resa.status }}</td>
                  <td v-if="displayUser">{{ users[resa.user].username }}</td>
                  <td v-if="displayProject">
                    {{ resa.project ? projects[resa.project].name : "" }}
                  </td>
                </tr>
              </template>
            </tbody>
          </table>
          <h4>Supply Usages</h4>
          <table class="table">
            <thead class="table-light">
              <tr>
                <th>Date</th>
                <th>Quantity</th>
                <th>validated</th>
                <th v-if="displayUser">User</th>
                <th v-if="displayProject">Project</th>
              </tr>
            </thead>
            <tbody>
              <template v-for="supply in supplyUsages">
                <tr>
                  <th>{{ supply.name }}</th>
                  <th>{{ supply.total + " " + supply.unit }}</th>
                  <th colspan="3"></th>
                </tr>
                <tr v-for="su in supply.usages">
                  <td>{{ formatDate(resadict[su.reservation].start_date) }}</td>
                  <td>{{ su.quantity + " " + supply.unit }}</td>
                  <td>
                    <svg v-show="su.validated" class="svg-icon-small">
                      <use href="#check" />
                    </svg>
                    <svg v-show="!su.validated" class="svg-icon-small">
                      <use href="#cross" />
                    </svg>
                  </td>
                  <td v-if="displayUser">
                    {{ users[resadict[su.reservation].user].username }}
                  </td>
                  <td v-if="displayProject">
                    {{
                      resadict[su.reservation].project
                        ? projects[resadict[su.reservation].project].name
                        : ""
                    }}
                  </td>
                </tr>
              </template>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onBeforeMount } from "vue";
import { useStore } from "vuex";
import { useRoute } from "vue-router";
import spacetime from "spacetime";
import ApiService from "@/common/api.service";
import Multiselect from "@vueform/multiselect";

const store = useStore();
const route = useRoute();

let title = "Usages"
const reservations = ref({});
let resadict = {};
const supplyUsages = ref({});
const users = ref({});
const projects = ref({});
const loaded = ref(false);
const displayUser = ref(true);
const displayProject = ref(true);

const fProject = ref(null);
const fUser = ref(null);
const fMinDate = ref(
  spacetime(new Date(new Date().getFullYear(), 0, 1)).format(
    "{year}-{iso-month}-{date-pad}"
  )
);
const fMaxDate = ref(
  spacetime(new Date(new Date().getFullYear(), 11, 31)).format(
    "{year}-{iso-month}-{date-pad}"
  )
);
const fType = ref(null);
const fStatus = ref(null);
const fValidated = ref(null);

const resaTypes = computed(() => store.getters["reservation_types/list"]);
const projectsOptions = computed(() => store.getters["projects/list"]);

async function findUser(query) {
  let users = await store.dispatch("users/fetchList", {
    params: { search: query },
  });
  return users.map((u) => {
    return {
      label: "@" + u.username + " " + u.first_name + " " + u.last_name,
      value: u.id,
    };
  });
}
function formatDate(startdate) {
  return spacetime(startdate).format(
    "{year}-{iso-month}-{date-pad} {hour-24-pad}:{minute-pad}"
  );
}

async function fetchUsages() {
  let params = {};
  if (fProject.value) {
    params.project = fProject.value == -1 ? null : fProject.value;
  }
  if (fUser.value) params.user = fUser.value;
  if (fType.value) params.type = fType.value;
  if (fStatus.value) params.status = fStatus.value;
  if (fValidated.value) params.validated = fValidated.value;
  if (fMinDate.value) params.mindate = spacetime(fMinDate.value).format("iso");
  if (fMaxDate.value) params.maxdate = spacetime(fMaxDate.value).format("iso");
  loaded.value = false;
  const { data } = await ApiService.query("/usages", params);
  reservations.value = data.reservations;
  for (let [key, value] of Object.entries(data.reservations)) {
    Object.assign(resadict, value.usages);
  }
  supplyUsages.value = data.supplies;
  users.value = data.users;
  projects.value = data.projects;
  loaded.value = true;
}

onBeforeMount(async () => {
  await store.dispatch("resources/fetchResources");
  if (route.name != "projectusages") store.dispatch("projects/fetchList");
  else {
    displayProject.value = false;
    fProject.value = route.params[route.meta.routeparam];
  }
  if (route.name == "myusages") {
    title="My Usages"
    displayUser.value = false;
    fUser.value = store.getters.authUser.id;
  }
  else if (route.name == "userusages") {
    displayUser.value = false;
    fUser.value = route.params[route.meta.routeparam];
  }

});
</script>
<style>
@import "@vueform/multiselect/themes/default.css";
.multiselect {
  min-width: 15em;
}
.multiselect .multiselect__content-wrapper {
  min-width: 100%;
  width: auto;
  border: none;
  box-shadow: 4px 4px 10px 0 rgba(0, 0, 0, 0.1);
}

.multiselect--active .multiselect__tags {
  border-bottom: none;
}
</style>
