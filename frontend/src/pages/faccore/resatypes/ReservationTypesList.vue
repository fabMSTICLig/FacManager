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
          <div class="row justify-content-between">
            <h3 class="col-auto">
              Reservation Types
            </h3>
            <div class="col-auto">
              <router-link
                class="btn btn-primary float-end"
                role="button"
                :to="{ name: 'resatype', params: { resatypeid: 'new' } }"
              >
                Add
              </router-link>
            </div>
          </div>
        </div>
        <div class="card-body">
          <form class="row row-cols-lg-auto g-3 align-items-center">
            <div class="col-12">
              <label
                class="form-label visually-hidden"
                for="searchInput"
              >Search</label>
              <input
                id="searchInput"
                v-model="searchInput"
                class="form-control"
                type="search"
                placeholder="Search"
              >
            </div>
          </form>
          <div class="table-responsive">
            <table class="table table-hover">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Need manager</th>
                  <th />
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="item in objects"
                  :key="item.id"
                >
                  <td v-text="item.name" />
                  <td>
                    <svg
                      v-show="item.need_manager"
                      class="svg-icon"
                    >
                      <use href="#check" />
                    </svg>
                    <svg
                      v-show="!item.need_manager"
                      class="svg-icon"
                    >
                      <use href="#cross" />
                    </svg>
                  </td>
                  <td class="text-end">
                    <router-link
                      class="btn btn-primary"
                      role="button"
                      :to="{
                        name: 'resatype',
                        params: { resatypeid: item.id },
                      }"
                    >
                      Update
                    </router-link>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <pagination
            :total="totalCount"
            :per-page="perPage"
            :current-page="currentPage"
            @pagechanged="onPageChange"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onBeforeMount } from "vue";
import useDebouncedRef from "@/composables/useDebouncedRef";
import { storeToRefs } from "pinia";
import { useReservationTypesStore } from "@/stores/reservations";

import useSearchStorage from "@/composables/useSearchStorage";
import Pagination from "@/components/nav/ListPagination.vue";

const store = useReservationTypesStore();
const { objects, count: totalCount } = storeToRefs(store);

const loaded = ref(false);
const searchInput = useDebouncedRef("");
const currentPage = ref(1);
const perPage = ref(parseInt(import.meta.env.VITE_APP_MAXLIST));

function onPageChange(page) {
  currentPage.value = page;
}

async function fetch(params) {
  await store.fetchList({ ...params });
}

const { refresh } = useSearchStorage(
  "resatypes",
  fetch,
  { search: searchInput },
  currentPage,
  perPage.value,
);

onBeforeMount(async () => {
  await refresh();
  loaded.value = true;
});
</script>
