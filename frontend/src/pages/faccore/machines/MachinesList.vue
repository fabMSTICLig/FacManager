<template>
  <div class="row">
    <div class="col-12 col-md-6">
      <div class="card">
        <div class="card-header">
          <div class="row  justify-content-between">
            <div class="col-6">
              <input
                v-model="searchInput"
                class="form-control"
                type="search"
                placeholder="Search"
              >
            </div>
            <div class="col-auto">
              <router-link
                class="btn btn-primary float-end"
                role="button"
                :to="{ name: 'machine', params: { machineid: 'new' } }"
              >
                Add
              </router-link>
            </div>
          </div>
        </div>
        <div class="card-body">
          <div class="table-responsive">
            <table class="table table-hover">
              <thead>
                <tr>
                  <th>Name</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="item in objectsList"
                  :key="item.id"
                  @click="selectedObject = item"
                >
                  <td v-text="item.name" />
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
      <div
        v-if="selectedObject"
        class="card"
      >
        <div class="card-header">
          <h3
            class="float-start"
            v-text="selectedObject.name"
          />
          <div
            class="btn-group float-end"
            role="group"
          >
            <router-link
              class="btn btn-primary"
              role="button"
              :to="{
                name: 'machine',
                params: { machineid: selectedObject.id },
              }"
            >
              Update
            </router-link>
          </div>
        </div>
        <div class="card-body">
          <p class="card-text">
            {{ selectedObject.description }}
          </p>
          <h5>Instances</h5>
          <DisplayIdList :items="selectedObject.instances" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onBeforeMount } from "vue";
import { useStore } from "vuex";

import useListFSP from "@/composables/useListFSP";
import Pagination from "@/components/nav/ListPagination.vue";
import DisplayIdList from "@/components/ui/DisplayIdList.vue";

const store = useStore();

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
} = useListFSP("machine_models");

onBeforeMount(() => {
    loadPage();
    return fetchList();
});
</script>
