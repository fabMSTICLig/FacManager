<template>
  <modal
    id="modal-availability"
    :show="true"
    v-show="show"
    title="Availability"
    :resolve="resolveModal"
    hide-footer
  >
    <form ref="form" @submit.prevent="handleSubmit">
      <div
        class="invalid-feedback d-block"
        ref="availability_errors"
        v-if="errors"
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
                class="form-control"
                id="availability-startdate"
                v-model="date_date"
                type="date"
                required
              />
            </div>
            <div class="col">
              <input
                class="form-control"
                id="availability-starttime"
                v-model="date_time"
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
                class="form-control"
                id="availability-enddate"
                v-model="enddate_date"
                type="date"
                required
              />
            </div>
            <div class="col">
              <input
                class="form-control"
                id="availability-endtime"
                v-model="enddate_time"
                type="time"
                :step="MIN_START_MINUTE"
                required
              />
            </div>
          </div>
        </div>
        <div class="mb-3" v-if="!object.id">
          <label for="occurence">Occurence:</label>
          <input
            class="form-control"
            id="occurence"
            v-model="object.occurence"
            type="number"
            min="1"
            required
          />
        </div>
        <div class="mb-3">
          <label for="avail-resources">Resources:</label>
          <div class="input-group">
            <select
              class="form-control"
              id="avail-ressource"
              v-model="object.resources"
              multiple
              :select-size="10"
              required
            >
              <option v-for="v in machines" :value="v.id" :key="v.id">
                {{ v.name }}
              </option>
              <option v-for="v in managers" :value="v.id" :key="v.id">
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
