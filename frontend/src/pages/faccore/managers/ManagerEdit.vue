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
                for="email"
              >Email</label>
              <input
                id="email"
                v-model="object.email"
                class="form-control"
                type="email"
              >
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
  useEditor("managers", { name: "", email: "" }, "Manager");

const cardName = computed(() =>
  isNew.value ? "New manager" : object.value.name
);

const route = useRoute();

onBeforeMount(() => {
    return initObject(route);
});
</script>
