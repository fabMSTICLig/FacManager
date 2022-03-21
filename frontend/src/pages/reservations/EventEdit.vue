<template>
  <modal
    id="modal-event"
    :show="true"
    v-show="show"
    title="Event"
    :resolve="resolveModal"
    hide-footer
  >
    <form ref="form" @submit.prevent="handleSubmit">
      <div class="invalid-feedback d-block" ref="event_errors" v-if="errors">
        <ul class="error-messages">
          <li v-for="e in errors" :key="e">{{ e }}</li>
        </ul>
      </div>
      <fieldset>
        <div class="mb-3">
          <label class="form-label" for="name">Name</label>
          <input
            id="name"
            ref="inputname"
            v-model="object.name"
            class="form-control"
            type="text"
            required
          />
        </div>

        <div class="mb-3">
          <label for="event-startdate">Start date:</label>
          <div class="form-row">
            <div class="col">
              <input
                class="form-control"
                id="event-startdate"
                v-model="date_date"
                type="date"
                required
              />
            </div>
            <div class="col">
              <input
                class="form-control"
                id="event-starttime"
                v-model="date_time"
                type="time"
                :step="MIN_START_MINUTE"
                required
              />
            </div>
          </div>
        </div>
        <div class="mb-3">
          <label for="event-enddate">End date:</label>
          <div class="form-row">
            <div class="col">
              <input
                class="form-control"
                id="event-enddate"
                v-model="enddate_date"
                type="date"
                required
              />
            </div>
            <div class="col">
              <input
                class="form-control"
                id="event-endtime"
                v-model="enddate_time"
                type="time"
                :step="MIN_START_MINUTE"
                required
              />
            </div>
          </div>
        </div>

        <div class="mb-3">
          <label for="event-desc">Description (Optional):</label>
          <textarea
            class="form-control"
            id="event-desc"
            v-model="object.commentary"
            placeholder="Description"
          ></textarea>
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

const object = ref({});
const inputname = ref();

function resolveModal() {
  show.value = false;
}

watch(show, async ()=>{
  if(show.value)
  {
    await nextTick()
    inputname.value.focus()
    inputname.value.scrollIntoView(false)
  }
})

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

function newEvent(startDate, endDate) {
  object.value = {};
  object.value.start_date = startDate;
  object.value.end_date = endDate;
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
    await store.dispatch("events/destroy", {
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
        await store.dispatch("events/update", {
          id: object.value.id,
          data: object.value,
        })
      );
    } else {
      emit(
        "created",
        await store.dispatch("events/create", { data: object.value })
      );
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
