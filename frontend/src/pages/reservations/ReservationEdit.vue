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
    id="modal-reservation"
    :show="true"
    title="Reservation"
    :resolve="resolveModal"
    hide-footer
  >
    <form ref="form" @submit.prevent="handleSubmit">
      <div v-if="errors" ref="resa_errors" class="invalid-feedback d-block">
        <ul class="error-messages">
          <li v-for="e in errors" :key="e">{{ e }}</li>
        </ul>
      </div>
      <div class="row">
        <fieldset class="col-12 col-md-6" :disabled="reservationReadOnly">
          <template v-if="isAdmin">
            <div class="mb-3">
              <label class="form-label" for="resa-user">User :</label>
              <Multiselect
                id="resa-user"
                ref="msuser"
                v-model="object.user"
                placeholder="Select a user"
                :filter-results="false"
                :min-chars="3"
                :resolve-on-load="false"
                :delay="1"
                :searchable="true"
                :options="findUser"
              />
            </div>
            <div class="mb-3">
              <label for="resa-status">Status:</label>
              <div class="input-group">
                <select
                  id="resa-status"
                  v-model="object.status"
                  class="form-control"
                  required
                >
                  <option>Requested</option>
                  <option>Accepted</option>
                  <option>Denied</option>
                  <option>Changed</option>
                </select>
              </div>
            </div>
          </template>
          <div v-show="pasteDate" class="alert alert-warning">
            <strong>Warning!</strong> The date is in the past.
          </div>
          <div class="mb-3">
            <label for="resa-startdate">Start date:</label>
            <div class="form-row">
              <div class="col">
                <input
                  id="resa-startdate"
                  v-model="date_date"
                  class="form-control"
                  type="date"
                  required
                />
              </div>
              <div class="col">
                <input
                  id="resa-starttime"
                  v-model="date_time"
                  class="form-control"
                  type="time"
                  :min="isAdmin ? '' : START_HOUR"
                  :max="isAdmin ? '' : END_HOUR"
                  :step="MIN_START_MINUTE"
                  required
                />
              </div>
            </div>
          </div>
          <div class="mb-3">
            <label for="resa-duration">Duration:</label>
            <div class="input-group">
              <input
                id="resa-duration"
                v-model="duration"
                class="form-control"
                type="number"
                :min="reservationType.min_time_slot"
                :step="reservationType.min_time_slot"
                required
              />
              <div class="input-group-append">
                <div class="input-group-text">h</div>
              </div>
            </div>
          </div>
          <div class="mb-3">
            <label for="resa-comm">Commentary (Optional):</label>
            <textarea
              id="resa-comm"
              v-model="object.commentary"
              class="form-control"
              placeholder="Commentary"
            ></textarea>
          </div>
          <div class="mb-3">
            <label for="resa-project">Project (Optional):</label>
            <select
              id="resa-project"
              v-model="object.project"
              class="form-control"
            >
              <option></option>
              <option
                v-for="project in projects"
                :key="project.id"
                :value="project.id"
                v-text="project.name"
              ></option>
            </select>
          </div>
        </fieldset>
        <div class="col-12 col-md-6">
          <div class="row">
            <fieldset class="col-12" :disabled="reservationReadOnly">
              <div class="mb-3">
                <label for="resa-type">Type:</label>
                <div class="input-group">
                  <select
                    id="resa-type"
                    ref="typeInput"
                    v-model="object.reservation_type"
                    class="form-control"
                    required
                  >
                    <option
                      v-for="rtype in allowedTypes"
                      :key="rtype.id"
                      :value="rtype.id"
                    >
                      {{ rtype.name }}
                    </option>
                  </select>
                </div>
              </div>
              <div
                v-for="mc in machinesChoices"
                :key="mc.model.name"
                class="mb-3"
              >
                <label v-text="mc.model.name"></label>
                <select v-model="mc.selected" class="form-control" required>
                  <option
                    v-for="m in mc.model.instances"
                    :key="m.id"
                    :value="m.id"
                    v-text="m.name"
                  />
                </select>
              </div>
              <div v-if="reservationType.need_manager" class="mb-3">
                <label for="resa-manager">Manager:</label>
                <div class="input-group">
                  <select
                    id="resa-manager"
                    v-model="object.manager"
                    class="form-control"
                    required
                  >
                    <option
                      v-for="manager in managers"
                      :key="manager.id"
                      :value="manager.id"
                    >
                      {{ manager.name }}
                    </option>
                  </select>
                </div>
              </div>
            </fieldset>
            <div v-if="object.id && addSU != null" class="col-12">
              <table class="table">
                <thead>
                <tr>
                  <th>Supply</th>
                  <th>Quantity</th>
                  <th v-if="isAdmin"></th>
                  <th></th>
                </tr>
              </thead>
            <tbody>
                <tr>
                  <td>
                    <select v-model="addSU.supply" class="form-control w-auto">
                      <option
                        v-for="supply in supplies"
                        :key="supply.id"
                        :value="supply.id"
                      >
                        {{ supply.name }}
                      </option>
                    </select>
                  </td>
                  <td>
                    <div class="input-group">
                      <input
                        v-model="addSU.quantity"
                        type="number"
                        min="0"
                        class="form-control"
                      /><span class="input-group-text">{{
                        getSupplyUnit(addSU.supply)
                      }}</span>
                    </div>
                  </td>
                  <td v-if="isAdmin"></td>

                  <td>
                    <div class="btn-group col-auto" role="group">
                    <button
                      class="btn btn-primary btn-sm"
                      type="button"
                      @click="addSupplyUsage()"
                    >
                      Add
                    </button>
                  </div>
                  </td>
                </tr>

                <tr v-for="su in supplyUsages" :key="su.id">
                  <td>
                    <select
                      v-model="su.supply"
                      class="form-control w-auto"
                      :readonly="!isAdmin && su.validated"
                    >
                      <option
                        v-for="supply in supplies"
                        :key="supply.id"
                        :value="supply.id"
                      >
                        {{ supply.name }}
                      </option>
                    </select>
                  </td>
                  <td>
                    <div class="input-group">
                      <input
                        v-model="su.quantity"
                        type="number"
                        min="0"
                        class="form-control"
                        :readonly="!isAdmin && su.validated"
                      /><span class="input-group-text">{{
                        getSupplyUnit(su.supply)
                      }}</span>
                    </div>
                  </td>
                  <td v-if="isAdmin">
                    <div>
                      <div class="form-check form-switch">
                        <input
                          v-model="su.validated"
                          type="checkbox"
                          class="form-check-input"
                        />
                      </div>
                    </div>
                  </td>

                  <td>
                    <div v-if="!isAdmin && su.validated">Validated</div>
                    <div v-else class="btn-group col-auto" role="group">
                      <button
                        class="btn btn-primary btn-sm"
                        type="button"
                        @click="updateSupplyUsage(su)"
                      >
                        <svg class="svg-icon-small">
                          <use href="#update" />
                        </svg>
                      </button>
                      <button
                        class="btn btn-danger btn-sm"
                        type="button"
                        @click="deleteSupplyUsage(su)"
                      >
                        <svg class="svg-icon-small">
                          <use href="#delete" />
                        </svg>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
      <div>
        <button
          v-if="object.id && isAdmin"
          class="btn btn-danger"
          type="button"
          @click="deleteResa"
        >
          Delete
        </button>

        <button class="btn btn-secondary" type="button" @click="show = false">
          {{ reservationReadOnly ? "Close" : "Cancel" }}
        </button>
        <button
          v-if="!reservationReadOnly"
          type="submit"
          :disabled="waiting"
          class="btn btn-primary"
        >
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
import Multiselect from "@vueform/multiselect";

import Modal from "@/plugins/modal";

const emit = defineEmits(["interfaces", "created", "updated", "deleted"]);
const store = useStore();

const authUser = computed(() => store.getters.authUser);
const isAdmin = computed(() => store.getters.isAdmin);

const START_HOUR = import.meta.env.VITE_APP_START_HOUR;
const END_HOUR = import.meta.env.VITE_APP_END_HOUR;
const MIN_START_MINUTE = import.meta.env.VITE_APP_MIN_START_MINUTE * 60;

const show = ref(false);
const waiting = ref(false);
const typeInput = ref();
const errors = ref([]);

const object = ref({ uses: [] });

watch(show, async () => {
  if (show.value) {
    await nextTick();
    typeInput.value.focus();
    typeInput.value.scrollIntoView(false);
  }
});

function resolveModal() {
  show.value = false;
}

const reservationReadOnly = computed(() => {
  return !(
    isAdmin.value ||
    object.value.status == "Requested" ||
    object.value.status === undefined
  );
});

const msuser = ref();
async function findUser(query) {
  let users = await store.dispatch("users/fetchList", {
    params: { search: query },
  });
  return users.map((u) => {
    return {
      label: "@" + u.username + " " + u.first_name + " " + u.last_name,
      value: u.id,
    };
  });
}

const allowedTypes = computed(() => {
  if (isAdmin.value) return store.getters["reservation_types/list"];
  else {
    return store.getters["reservation_types/list"].filter((rt) => {
      if (rt.need_manager) return true;
      else {
        return !rt.needs.some(
          (mmid) => store.getters["training_levels/byId"](mmid).need_manager
        );
      }
    });
  }
});
const reservationType = computed(() => {
  return (
    store.getters["reservation_types/byId"](object.value.reservation_type) || {
      need_manager: false,
      needs: [],
    }
  );
});
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
    object.value.end_date = spacetime(value)
      .time(spacetime(object.value.end_date).time())
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
    var diff = spacetime(object.value.start_date).diff(
      spacetime(object.value.end_date),
      "minutes"
    );
    let newvalue = spacetime(object.value.start_date).time(value);
    object.value.start_date = newvalue.format("iso");
    object.value.end_date = newvalue.add(diff, "minutes").format("iso");
  },
});
const pasteDate = computed(() => {
  return Date.parse(object.value.start_date) - Date.now() < 0 && (object.value.status == "Requested" || ! object.value.id);
});
const duration = computed({
  get: function () {
    return (
      (Date.parse(object.value.end_date) -
        Date.parse(object.value.start_date)) /
      3600000
    );
  },
  set: function (value) {
    object.value.end_date = spacetime(object.value.start_date)
      .add(value * 60, "minutes")
      .format("iso");
  },
});

const managers = computed(() => store.getters["managers/list"]);

const machinesChoices = computed(() => {
  let mc = {};
  reservationType.value.needs.forEach((mmid) => {
    let mm = store.getters["machine_models/byId"](mmid);
    mc[mmid] = { model: mm, selected: null };
    mm.instances.some((i) => {
      if (object.value.uses.indexOf(i.id) > -1) {
        mc[mmid].selected = i.id;
        return true;
      } else return false;
    });
  });
  return mc;
});

const projects = computed(() => store.getters["projects/list"]);

function newResa(startDate, endDate, resource) {
  object.value = {
    start_date: startDate,
    end_date: endDate,
    manager: null,
  };
  if (isAdmin.value) {
    object.value.status = "Accepted";
  }
  object.value.user = authUser.value.id;
  if ("model" in resource.extendedProps)
    object.value.uses = [parseInt(resource.id)];
  else object.value.uses = [];
  initResa();
}

async function updateResa(resa) {
  object.value = Object.assign(
    {},
    await store.dispatch("reservations/fetchSingle", {
      id: resa.id,
    })
  );
  await store.dispatch("supply_usages/fetchList", {
    prefix: "/reservations/" + resa.id + "/",
  });
  initResa();
}

async function initResa() {
  errors.value = [];
  store.dispatch("projects/fetchList", {
    params: { afterdate: object.value.start_date },
  });
  if (object.value.user && isAdmin.value) {
    const u = await store.dispatch("users/fetchSingle", {
      id: object.value.user,
    });
    msuser.value.select({
      label: "@" + u.username + " " + u.first_name + " " + u.last_name,
      value: u.id,
    });
  }
  show.value = true;
}

onMounted(() => {
  emit("interfaces", { newResa, updateResa });
});

async function deleteResa() {
  errors.value = [];
  waiting.value = true;
  try {
    await store.dispatch("reservations/destroy", {
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
  let uses = [];
  for (const [key, mc] of Object.entries(machinesChoices.value)) {
    if (mc.selected) uses.push(mc.selected);
  }
  object.value.uses = uses;
  waiting.value = true;
  try {
    if (object.value.id) {
      emit(
        "updated",
        await store.dispatch("reservations/update", {
          id: object.value.id,
          data: object.value,
        })
      );
    } else {
      emit(
        "created",
        await store.dispatch("reservations/create", { data: object.value })
      );
    }
    show.value = false;
  } catch (e) {
    if (e.response.status == 400)
      if(e.response.data.non_field_errors)
        errors.value = errors.value.concat(e.response.data.non_field_errors);
      else if(Array.isArray(e.response.data))
        errors.value = errors.value.concat(e.response.data);
  }
  waiting.value = false;
}

//////////////Supply Usages/////////

onBeforeMount(() => {
  store.dispatch("supplies/fetchUnits");
});

const supplyUnits = computed(() => store.getters["supplies/units"]);
const supplyUsages = computed(() => store.getters["supply_usages/list"]);
const supplies = computed(() => store.getters["supplies/list"]);
function getSupplyUnit(supplyid) {
  let supply = store.getters["supplies/byId"](supplyid);
  if (supply) return supplyUnits.value[supply.unit];
  else return "";
}
const addSU = ref(null);
if(supplies.value.length)
{
  addSU.value={quantity:1, supply:supplies.value[0].id};
}

function addSupplyUsage()
{
  store.dispatch("supply_usages/create",{prefix:"/reservations/"+object.value.id+"/", data:addSU.value})
}

function updateSupplyUsage(su)
{
  store.dispatch("supply_usages/update",{prefix:"/reservations/"+object.value.id+"/", data:su, id:su.id})
}
function deleteSupplyUsage(su)
{
  store.dispatch("supply_usages/destroy",{prefix:"/reservations/"+object.value.id+"/", id:su.id})
}

</script>
<style>
.modal-dialog {
  max-width: 1000px;
}
</style>
