<!--
Copyright (C) 2020-2022 LIG Université Grenoble Alpes


This file is part of FacManager.

FacManager is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

FacManager is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with FacManager. If not, see <https://www.gnu.org/licenses/>

@author Germain Lemasson
-->

<template>
  <modal
    v-show="show"
    id="modal-availability"
    :show="true"
    title="Availability"
    :resolve="resolveModal"
    hide-footer
  >
    <form ref="form" @submit.prevent="handleSubmit">
      <div
        v-if="errors"
        ref="availability_errors"
        class="invalid-feedback d-block"
      >
        <ul class="error-messages">
          <li v-for="e in errors" :key="e">{{ e }}</li>
        </ul>
      </div>
      <fieldset>
        <div class="mb-3">
          <label for="availability-startdate">Start date:</label>
          <div class="form-row">
            <div class="col">
              <input
                id="availability-startdate"
                v-model="date_date"
                class="form-control"
                type="date"
                required
              />
            </div>
            <div class="col">
              <input
                id="availability-starttime"
                v-model="date_time"
                class="form-control"
                type="time"
                :step="MIN_START_MINUTE"
                required
              />
            </div>
          </div>
        </div>
        <div class="mb-3">
          <label for="availability-enddate">End date:</label>
          <div class="form-row">
            <div class="col">
              <input
                id="availability-enddate"
                v-model="enddate_date"
                class="form-control"
                type="date"
                required
              />
            </div>
            <div class="col">
              <input
                id="availability-endtime"
                v-model="enddate_time"
                class="form-control"
                type="time"
                :step="MIN_START_MINUTE"
                required
              />
            </div>
          </div>
        </div>
        <div v-if="!object.id" class="mb-3">
          <label for="occurence">Occurence:</label>
          <input
            id="occurence"
            v-model="object.occurence"
            class="form-control"
            type="number"
            min="1"
            required
          />
        </div>
        <div class="mb-3">
          <label for="avail-resources">Resources:</label>
          <div class="input-group">
            <select
              id="avail-ressource"
              v-model="object.resources"
              class="form-control"
              multiple
              :select-size="10"
              required
            >
              <option v-for="v in machines" :key="v.id" :value="v.id">
                {{ v.name }}
              </option>
              <option v-for="v in managers" :key="v.id" :value="v.id">
                {{ v.name }}
              </option>
            </select>
          </div>
        </div>
      </fieldset>
      <div>
        <button
          v-if="object.id"
          class="btn btn-danger"
          type="button"
          @click="deleteAvailability"
        >
          Delete
        </button>

        <button class="btn btn-secondary" type="button" @click="show = false">
          Cancel
        </button>
        <button type="submit" :disabled="waiting" class="btn btn-primary">
          Ok
        </button>
      </div>
    </form>
  </modal>
</template>
<script setup>
import { ref, computed, watch, nextTick, onBeforeMount, onMounted } from "vue";
import { useStore } from "vuex";
import spacetime from "spacetime";

import Modal from "@/plugins/modal";

const emit = defineEmits(["interfaces", "created", "updated", "deleted"]);
const store = useStore();
const MIN_START_MINUTE = import.meta.env.VITE_APP_MIN_START_MINUTE * 60;

const show = ref(false);
const waiting = ref(false);
const errors = ref([]);

const object = ref({ resources: [] });

function resolveModal() {
  show.value = false;
}
const date_date = computed({
  get: function () {
    return spacetime(object.value.start_date).format(
      "{year}-{iso-month}-{date-pad}"
    );
  },
  set: function (value) {
    object.value.start_date = spacetime(value)
      .time(spacetime(object.value.start_date).time())
      .format("iso");
  },
});
const date_time = computed({
  get: function () {
    return spacetime(object.value.start_date).format(
      "{hour-24-pad}:{minute-pad}"
    );
  },
  set: function (value) {
    object.value.start_date = spacetime(object.value.start_date)
      .time(value)
      .format("iso");
  },
});
const enddate_date = computed({
  get: function () {
    return spacetime(object.value.end_date).format(
      "{year}-{iso-month}-{date-pad}"
    );
  },
  set: function (value) {
    object.value.end_date = spacetime(value)
      .time(spacetime(object.value.end_date).time())
      .format("iso");
  },
});
const enddate_time = computed({
  get: function () {
    return spacetime(object.value.end_date).format(
      "{hour-24-pad}:{minute-pad}"
    );
  },
  set: function (value) {
    object.value.end_date = spacetime(object.value.end_date)
      .time(value)
      .format("iso");
  },
});

const managers = computed(() => store.getters["managers/list"]);
const machines = computed(() => store.getters["machines/list"]);

function newAvailability(startDate, endDate, resource) {
  object.value = {
    occurence: 1,
    resources: [resource.id],
    start_date: startDate,
    end_date: endDate,
  };
  initAvailability();
}

function updateAvailability(availability) {
  object.value = Object.assign({}, availability);
  initAvailability();
}

async function initAvailability() {
  errors.value = [];
  show.value = true;
}

onMounted(() => {
  emit("interfaces", { newAvailability, updateAvailability });
});

async function deleteAvailability() {
  errors.value = [];
  waiting.value = true;
  try {
    await store.dispatch("availabilities/destroy", {
      id: object.value.id,
    });
    emit("deleted", object.value.id);
    show.value = false;
  } catch (e) {
    console.log(e.response);
  }
  waiting.value = false;
}
async function handleSubmit() {
  errors.value = [];
  waiting.value = true;
  try {
    if (object.value.id) {
      emit(
        "updated",
        await store.dispatch("availabilities/update", {
          id: object.value.id,
          data: object.value,
        })
      );
    } else {
      emit("created", {
        avail: await store.dispatch("availabilities/create", {
          data: object.value,
        }),
        refresh: object.value.occurence > 1,
      });
    }
    show.value = false;
  } catch (e) {
    if ("response" in e) {
      if (e.response.status == 400)
        errors.value = errors.value.concat(e.response.data.non_field_errors);
    } else {
      console.log(e);
    }
  }
  waiting.value = false;
}
</script>
