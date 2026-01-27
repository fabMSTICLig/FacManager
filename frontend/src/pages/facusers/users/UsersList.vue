<template>
  <div class="row">
    <div class="col-12">
      <div class="card">
        <div class="card-header">
          <div class="row justify-content-between">
            <h3 class="col-auto">
              Utilisateurs
            </h3>
          </div>
        </div>
        <div class="card-body">
          <form class="row row-cols-lg-auto g-3 align-items-center">
            <div class="col-12">
              <label
                class="form-label visually-hidden"
                for="searchInput"
              >Chercher</label>
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
                  <th>Nom utilisateur</th>
                  <th>Prénom Nom</th>
                  <th>Validated</th>
                  <th />
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="item in objects"
                  :key="item.id"
                >
                  <td v-text="item.username" />
                  <td>
                    <a :href="'mailto:' + item.email">{{ item.first_name }} {{ item.last_name }}</a>
                  </td>
                  <td>
                    <svg
                      v-show="item.charter"
                      class="svg-icon"
                    >
                      <use href="#check" />
                    </svg>
                    <svg
                      v-show="!item.charter"
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
                        name: 'useredit',
                        params: { userid: item.id },
                      }"
                    >
                      Modifier
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
import { onBeforeMount, ref } from "vue";
import { storeToRefs } from "pinia";
import useDebouncedRef from "@/composables/useDebouncedRef";
import { useUsersStore } from "@/stores/users";

import Pagination from "@/components/nav/ListPagination.vue";
import useSearchStorage from "@/composables/useSearchStorage";

const store = useUsersStore();
const loaded = ref(false);

const { objects, count: totalCount } = storeToRefs(store);

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
  "users",
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
