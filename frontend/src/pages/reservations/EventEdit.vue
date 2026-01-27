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
    id="modal-event"
    :show="true"
    title="Event"
    :resolve="resolveModal"
    hide-footer
  >
    <form
      ref="form"
      @submit.prevent="handleSubmit"
    >
      <div
        v-if="errors"
        ref="event_errors"
        class="invalid-feedback d-block"
      >
        <ul class="error-messages">
          <li
            v-for="e in errors"
            :key="e"
          >
            {{ e }}
          </li>
        </ul>
      </div>
      <fieldset>
        <div class="mb-3">
          <label
            class="form-label"
            for="name"
          >Name</label>
          <input
            id="name"
            ref="inputname"
            v-model="object.name"
            class="form-control"
            type="text"
            required
          >
        </div>

        <div class="mb-3">
          <label for="event-startdate">Start date:</label>
          <div class="form-row">
            <div class="col input-group">
              <input
                id="event-startdate"
                v-model="date_date"
                class="form-control"
                type="date"
                required
              ><button
                v-if="!object.id"
                class="btn btn-sm input-group-append"
                :class="[willBulk ? 'btn-success' : 'btn-danger']"
                type="button"
                @click="showBulk = true"
              >
                Bulk
              </button>
            </div>
            <div class="col">
              <input
                id="event-starttime"
                v-model="date_time"
                class="form-control"
                type="time"
                :step="MIN_START_MINUTE"
                required
              >
            </div>
          </div>
        </div>
        <div class="mb-3">
          <label for="event-enddate">End date:</label>
          <div class="form-row">
            <div class="col">
              <input
                id="event-enddate"
                v-model="enddate_date"
                class="form-control"
                type="date"
                required
              >
            </div>
            <div class="col">
              <input
                id="event-endtime"
                v-model="enddate_time"
                class="form-control"
                type="time"
                :step="MIN_START_MINUTE"
                required
              >
            </div>
          </div>
        </div>

        <div class="mb-3">
          <label for="event-desc">Description (Optional):</label>
          <textarea
            id="event-desc"
            v-model="object.description"
            class="form-control"
            placeholder="Description"
          />
        </div>
        <div class="mb-3 form-check form-switch">
          <label
            class="form-check-label"
            for="check-closing"
          >Fermeture</label>
          <input
            id="check-closing"
            v-model="object.closing"
            type="checkbox"
            class="form-check-input"
          >
        </div>
      </fieldset>
      <div>
        <button
          v-if="object.id"
          class="btn btn-danger"
          type="button"
          @click="deleteEvent"
        >
          Delete
        </button>

        <button
          class="btn btn-secondary"
          type="button"
          @click="show = false"
        >
          Cancel
        </button>
        <button
          type="submit"
          :disabled="waiting"
          class="btn btn-primary"
        >
          Ok
        </button>
      </div>
      <modal
        id="modal-bulk"
        title="List of date"
        :show="showBulk"
        :resolve="() => (showBulk = false)"
      >
        <div class="mb-3">
          <label for="bulktxt">List of date format 2025-05-30, one per line</label>
          <textarea
            id="bulktxt"
            v-model="bulkTxt"
            class="form-control"
            placeholder="2025-05-23"
            rows="10"
          />
          <div
            v-show="wrongBulk"
            class="alert alert-warning"
          >
            <strong>Warning!</strong> Wrong format for bulk dates.
          </div>
        </div>
      </modal>
    </form>
  </modal>
</template>
<script setup>
import { ref, computed, watch, nextTick, onMounted } from "vue";
import { useEventsStore } from "@/stores/events";
import spacetime from "spacetime";

import Modal from "@/plugins/modal";

const emit = defineEmits(["interfaces", "created", "updated", "deleted"]);
const store = useEventsStore();
const MIN_START_MINUTE = import.meta.env.VITE_APP_MIN_START_MINUTE * 60;

const show = ref(false);
const waiting = ref(false);
const errors = ref([]);

const showBulk = ref(false);
const bulkTxt = ref("");

const object = ref({});
const inputname = ref();

function resolveModal() {
  show.value = false;
}

watch(show, async () => {
  if (show.value) {
    await nextTick();
    inputname.value.focus();
    inputname.value.scrollIntoView(false);
  }
});

const date_date = computed({
  get: function () {
    return spacetime(object.value.start_date).format(
      "{year}-{iso-month}-{date-pad}",
    );
  },
  set: function (value) {
    bulkTxt.value = spacetime(value).format("iso-short");
    object.value.start_date = spacetime(value)
      .time(spacetime(object.value.start_date).time())
      .format("iso");
  },
});
const date_time = computed({
  get: function () {
    return spacetime(object.value.start_date).format(
      "{hour-24-pad}:{minute-pad}",
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
      "{year}-{iso-month}-{date-pad}",
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
      "{hour-24-pad}:{minute-pad}",
    );
  },
  set: function (value) {
    object.value.end_date = spacetime(object.value.end_date)
      .time(value)
      .format("iso");
  },
});

const risodate = /\d{4}-[01]\d-[0-3]\d/;
const wrongBulk = computed(() => {
  let lines = bulkTxt.value.split("\n");
  let ok = true;
  for (var i = 0; i < lines.length; i++) {
    ok = ok && risodate.test(lines[i]);
  }
  return !ok;
});

const willBulk = computed(() => {
  return (
    !object.value.id && !wrongBulk.value && bulkTxt.value.split("\n").length > 1
  );
});

function newEvent(startDate, endDate) {
  object.value = {};
  object.value.start_date = startDate;
  object.value.end_date = endDate;
  bulkTxt.value = spacetime(startDate).format("iso-short");
  initEvent();
}

function updateEvent(event) {
  object.value = Object.assign({}, event);
  initEvent();
}

function initEvent() {
  errors.value = [];
  show.value = true;
}

onMounted(() => {
  emit("interfaces", { newEvent, updateEvent });
});

async function deleteEvent() {
  errors.value = [];
  waiting.value = true;
  try {
    await store.destroy(object.value.id);
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
  if (willBulk.value) {
    let lines = bulkTxt.value.split("\n");
    var listevent = [];
    for (var i = 0; i < lines.length; i++) {
      var value = lines[i];
      object.value.start_date = spacetime(value)
        .time(spacetime(object.value.start_date).time())
        .format("iso");
      object.value.end_date = spacetime(value)
        .time(spacetime(object.value.end_date).time())
        .format("iso");
      try {
        listevent.push(await store.create(object.value));
      } catch (e) {
        console.log(e);
      }
    }
    emit("created", listevent);
    show.value = false;
  } else {
    try {
      if (object.value.id) {
        emit("updated", await store.update(object.value.id, object.value));
      } else {
        emit("created", await store.create(object.value));
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
  }
  waiting.value = false;
}
</script>
