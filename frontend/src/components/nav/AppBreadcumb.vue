<!--
Copyright (C) 2020-2022 LIG Université Grenoble Alpes


This file is part of FacManager.

FacManager is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

FacManager is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with FacManager. If not, see <https://www.gnu.org/licenses/>

@author Germain Lemasson
-->

<template>
  <nav aria-label="breadcrumb">
    <ol class="breadcrumb">
      <router-link
        v-for="item in breaditems"
        :key="item.name"
        v-slot="{ href, navigate, isExactActive }"
        :to="{ name: item.name, params: item.params }"
        custom
      >
        <li
          class="breadcrumb-item"
          :class="[isExactActive && 'active']"
          :aria-current="[isExactActive && 'page']"
        >
          <a
            v-if="!isExactActive"
            :href="href"
            @click="navigate"
          >
            <span v-text="item.label" />
          </a>
          <span
            v-else
            v-text="item.label"
          />
        </li>
      </router-link>
    </ol>
  </nav>
</template>

<script setup>
import { ref, watch, onBeforeMount } from "vue";
import { useRoute } from "vue-router";
import { useStore } from "vuex";

const store = useStore();
const route = useRoute();

const breaditems = ref([]);
watch(route, () => updateItems(route));
function makeBreadItem(item, route, promises) {
  if ("breadcumb" in item.meta) {
    promises.push(
      new Promise((resolve) => {
        if (typeof item.meta.breadcumb.label == "string") {
          resolve({
            label: item.meta.breadcumb.label,
            name: item.meta.breadcumb.name,
          });
        } else {
          if (route.params[item.meta.routeparam] == "new") {
            resolve({
              label: "Création",
              name: item.meta.breadcumb.name,
              params: route.params,
            });
          } else {
            var prefix = "";
            if ("prefix" in item.meta.breadcumb.label) {
              item.meta.breadcumb.label.prefix.forEach((item) => {
                prefix += item.ressource + "/" + route.params[item.param] + "/";
              });
            }

            store
              .dispatch(item.meta.breadcumb.label.ressource + "/fetchSingle", {
                id: route.params[item.meta.routeparam],
                prefix: prefix,
              })
              .then((data) => {
                resolve({
                  label: data[item.meta.breadcumb.label.labelprop],
                  name: item.meta.breadcumb.name,
                  params: route.params,
                });
              });
          }
        }
      })
    );
  }
  /*
        Adding a suffix to current route
        for child component not to be resolved directly 
        TODO: find a workaround
      */
  if (item.meta.breadcumb) {
    if (item.meta.breadcumb.label.labelchild)
      promises.push(
        new Promise((resolve) => {
          resolve({
            label: item.meta.breadcumb.label.labelchild,
            name: "",
          });
        })
      );
  }
}
function updateItems(route) {
  let promises = [];
  breaditems.value = [];
  route.matched.forEach((item) => {
    makeBreadItem(item, route, promises);
  });
  Promise.all(promises).then((values) => {
    breaditems.value = values;
  });
}
onBeforeMount(() => {
  updateItems(route);
});


</script>
