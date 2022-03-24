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
            <div class="col-auto">
              <router-link
                class="btn btn-primary float-end"
                role="button"
                :to="{ name: 'projectedit', params: { projectid: 'new' } }"
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
                  <th>Type</th>
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
                  <td v-text="item.start_date" />
                  <td v-text="item.end_date" />
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
          <h3 class="float-start" v-text="selectedObject.name" />
          <div class="btn-group float-end" role="group">
            <router-link
              class="btn btn-primary"
              role="button"
              :to="{
                name: 'projectedit',
                params: { projectid: selectedObject.id },
              }"
            >
              Update
            </router-link>
            <router-link
              class="btn btn-primary"
              role="button"
              :to="{
                name: 'projectusages',
                params: { projectid: selectedObject.id },
              }"
            >
              Usages
            </router-link>
          </div>
        </div>
        <div class="card-body">
          <p class="card-text">
            {{ selectedObject.description }}
          </p>
          <p class="card-text">Start Date : {{ selectedObject.start_date }}</p>
          <p class="card-text">End Date : {{ selectedObject.end_date }}</p>
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
} = useListFSP("projects");

onBeforeMount(() => {
  loadPage();
  return fetchList();
});
</script>
