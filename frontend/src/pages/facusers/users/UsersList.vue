<template>
  <div class="row">
    <div class="col-12 col-md-6">
      <div class="card">
        <div class="card-header">
          <div class="row justify-content-between">
            <div class="col-6">
              <input
                v-model="searchInput"
                class="form-control"
                type="search"
                placeholder="Search"
              />
            </div>
          </div>
        </div>
        <div class="card-body">
          <div class="table-responsive">
            <table class="table table-hover">
              <thead>
                <tr>
                  <th>Name utilisateur</th>
                  <th>Prénom</th>
                  <th>Name</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="item in objectsList"
                  :key="item.id"
                  @click="selectedObject = item"
                >
                  <td v-text="item.username" />
                  <td v-text="item.first_name" />
                  <td v-text="item.last_name" />
                </tr>
              </tbody>
            </table>
          </div>
          <pagination
            :total-pages="pagesCount"
            :total="objectsCount"
            :per-page="perPage"
            :current-page="currentPage"
            @pagechanged="onPageChange"
          />
        </div>
      </div>
    </div>
    <div class="col-12 col-md-6">
      <div v-if="selectedObject" class="card">
        <div class="card-header">
          <h3 class="float-start" v-text="selectedObject.username" />
          <div class="btn-group float-end" role="group">
            <router-link
              class="btn btn-primary"
              role="button"
              :to="{ name: 'useredit', params: { userid: selectedObject.id } }"
            >
              Update </router-link
            ><router-link
              class="btn btn-primary"
              role="button"
              :to="{
                name: 'userusages',
                params: { userid: selectedObject.id },
              }"
            >
              Usages
            </router-link>
          </div>
        </div>
        <div class="card-body">
          <p class="card-text">
            <span
              ><strong>{{ selectedObject.username }} :&nbsp;</strong></span
            >{{ selectedObject.first_name }} {{ selectedObject.last_name }}
          </p>
          <p>
            <span><strong>Email :&nbsp;</strong></span
            ><a :href="'mailto:' + selectedObject.email">{{
              selectedObject.email
            }}</a>
          </p>
          <p class="card-text">
            Charter :
            <svg v-show="selectedObject.charter" class="svg-icon">
              <use href="#check" />
            </svg>
            <svg v-show="!selectedObject.charter" class="svg-icon">
              <use href="#cross" />
            </svg>
          </p>

          <h5>Organizations</h5>
          <DisplayIdList :items="selectedOrganizations" />
          <h5>Projects</h5>
          <DisplayIdList :items="selectedProjects" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, watch, onBeforeMount } from "vue";
import { useStore } from "vuex";

import DisplayIdList from "@/components/ui/DisplayIdList.vue";

import useListFSP from "@/composables/useListFSP";
import Pagination from "@/components/nav/ListPagination.vue";

const {
  selectedObject,
  searchInput,
  currentPage,
  pagesCount,
  perPage,
  onPageChange,
  loadPage,
  objectsList,
  objectsCount,
  fetchList,
} = useListFSP("users");

const store = useStore();

const selectedOrganizations = computed(
  () => store.getters["organizations/list"]
);
const selectedProjects = computed(() => store.getters["projects/list"]);

watch(selectedObject, () => {
  if (selectedObject.value) {
    if (selectedObject.value.organizations)
      store.dispatch("organizations/fetchList", {
        params: { ids: selectedObject.value.organizations.join(",") },
      });
    if (selectedObject.value.projects)
      store.dispatch("projects/fetchList", {
        params: { ids: selectedObject.value.projects.join(",") },
      });
  }
});

onBeforeMount(() => {
  loadPage();
  return fetchList();
});
</script>
