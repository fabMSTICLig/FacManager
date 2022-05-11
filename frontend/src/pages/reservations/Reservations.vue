<!--
Copyright (C) 2020-2022 LIG Université Grenoble Alpes


This file is part of FacManager.

FacManager is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

FacManager is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with FacManager. If not, see <https://www.gnu.org/licenses/>

@author Germain Lemasson
-->

<template>
  <div v-if="loaded" class="row">
    <div class="col-12">
      <FullCalendar ref="calendar" :options="calendarOptions" />
    </div>
    <div class="col col-12">
      <div class="fm-event-legend">
        <div>
          <strong>Opening Hours : </strong
        ><span
          >Monday 13:30 to 17:00, Tuesday-Friday 9:00 to 11:00 and 13:30 to
            17:00</span
        >
        </div>
        <div class="d-flex">
          <span class="avail-background p-2 text-dark">Resources availabilities</span>
        </div>
        <div class="d-flex text-light">
          <span class="event-background p-2">Event</span>
          <span
            v-for="(v, k) in RESA_COLORS"
            :key="k"
            class="fc-event p-2"
            :style="'background-color:' + v"
            v-text="'Reservation ' + k"
          ></span>
          <span class="p-2 text-dark" style="border: 1px solid red;" >My reservations</span>
        </div>
      </div>
    </div>

    <ReservationEdit
      @interfaces="resaInterfaces"
      @created="resaCreated"
      @deleted="resaDeleted"
      @updated="resaUpdated"
    />
    <EventEdit
      v-if="isAdmin"
      @interfaces="eventInterfaces"
      @created="eventCreated"
      @deleted="eventDeleted"
      @updated="eventUpdated"
    />
    <AvailabilityEdit
      v-if="isAdmin"
      @interfaces="availInterfaces"
      @created="availCreated"
      @deleted="availDeleted"
      @updated="availUpdated"
    />
    <modal
      id="modal-charter"
      title="Charter"
      :show="showCharter"
      :resolve="()=>showCharter=false"
    >
      <p>
        You must read the charter before you can make any reservation. <a :href="charterUrl">{{charterUrl}}</a>
      </p>
    </modal>

  </div>
</template>

<script setup>
import "@fullcalendar/core/vdom"; // solves problem with Vite
import FullCalendar from "@fullcalendar/vue3";
import resourceTimelinePlugin from "@fullcalendar/resource-timeline";
import dayGridPlugin from "@fullcalendar/daygrid";
import frLocale from "@fullcalendar/core/locales/fr";
import interactionPlugin from "@fullcalendar/interaction";

import { ref, computed, nextTick, watch, onBeforeMount, onMounted } from "vue";
import { useStore } from "vuex";

import ReservationEdit from "./ReservationEdit.vue";
import EventEdit from "./EventEdit.vue";
import AvailabilityEdit from "./AvailabilityEdit.vue";
import Modal from "@/plugins/modal";

const store = useStore();

const isAdmin = computed(() => store.getters.isAdmin);
const authUser = computed(() => store.getters.authUser);
const RESA_COLORS = JSON.parse(import.meta.env.VITE_APP_RESA_COLORS);

const loaded = ref(false);
const calendar = ref();
let calAPI = null;

const showCharter = ref(false)
const charterUrl = import.meta.env.VITE_APP_CHARTER_URL

const resources = ref([]);
const datesQuery = ref({});
const calEventsLoading = ref(false);
const modeAvail = ref(false);

onBeforeMount(async () => {
  await store.dispatch("resources/fetchResources");
  resources.value.push({ id: "event", title: "Events", group: "01 Events" });
  resources.value = resources.value.concat(
    store.getters["managers/list"].map((manager) => {
      return {
        id: manager.id,
        title: manager.name,
        group: "02 Managers",
        manager: manager,
      };
    })
  );
  store.getters["machine_models/list"].forEach((mm) => {
    mm.instances.forEach((i) => {
      resources.value.push({
        id: i.id,
        title: i.name,
        group: "1" + mm.display_order + " " + mm.name,
        model: mm,
        machine: i,
      });
    });
  });
  calendarOptions.resources = resources.value;
  loaded.value = true;
  await nextTick();
  calAPI = calendar.value.getApi();
  if(!authUser.value.charter) showCharter.value=true;
});

function eventToCalEvent(event) {
  return {
    title: event.name,
    start: event.start_date,
    end: event.end_date,
    id: "e" + event.id,
    event: event,
    resourceId: "event",
  };
}
function resaToCalEvent(resa) {
  let calEvent = {
    title:
      store.getters["reservation_types/byId"](resa.reservation_type).name +
      "\n" +
      resa.status,
    start: resa.start_date,
    end: resa.end_date,
    id: resa.id,
    color: RESA_COLORS[resa.status],
    own: resa.own,
    resourceIds: resa.uses.concat([resa.manager]),
    resa: resa,
  };
  if (resa.own) calEvent.borderColor = "red";
  return calEvent;
}
function availToCalEvent(avail) {
  return {
    start: avail.start_date,
    end: avail.end_date,
    id: "a" + avail.id,
    resourceIds: avail.resources,
    display: modeAvail.value ? "" : "background",
    availability: avail,
  };
}
function fetchCalEvents(dateInfo, success, failure) {
  datesQuery.value = {
    mindate: dateInfo.startStr,
    maxdate: dateInfo.endStr,
  };
  sessionStorage.setItem("start_date", dateInfo.startStr);
  Promise.all([
    store.dispatch("reservations/fetchList", { params: datesQuery.value }),
    store.dispatch("events/fetchList", { params: datesQuery.value }),
    store.dispatch("availabilities/fetchList", { params: datesQuery.value }),
  ]).then(() => {
    let ev = [];
    if (!modeAvail.value) {
      ev = store.getters["reservations/list"].map(resaToCalEvent);
    }
    ev = store.getters["availabilities/list"].map(availToCalEvent).concat(ev);
    ev = ev.concat(store.getters["events/list"].map(eventToCalEvent));
    success(ev);
  });
}

let resaCreate = null;
let resaUpdate = null;

function resaInterfaces(interfaces) {
  resaCreate = interfaces.newResa;
  resaUpdate = interfaces.updateResa;
}

function resaCreated(resa) {
  calAPI.addEvent(resaToCalEvent(resa), true);
}

function resaUpdated(resa) {
  let calEvent = calAPI.getEventById(resa.id);
  if (calEvent) {
    calEvent.setProp(
      "title",
      store.getters["reservation_types/byId"](resa.reservation_type).name +
        "\n" +
        resa.status
    );
    calEvent.setStart(resa.start_date);
    calEvent.setEnd(resa.end_date);
    calEvent.setExtendedProp("resa", resa);
    calEvent.setProp("color", RESA_COLORS[resa.status]);
    calEvent.setExtendedProp("own", resa.own);
    if (resa.own) calEvent.setProp("borderColor", "red");
    calEvent.setResources(resa.uses.concat(resa.manager ? [resa.manager]: []));
  }
}
function resaDeleted(resaId) {
  let calEvent = calAPI.getEventById(resaId);
  if (calEvent) calEvent.remove();
}

let eventCreate = null;
let eventUpdate = null;

function eventInterfaces(interfaces) {
  eventCreate = interfaces.newEvent;
  eventUpdate = interfaces.updateEvent;
}

function eventCreated(event) {
  calAPI.addEvent(eventToCalEvent(event), true);
}

function eventUpdated(event) {
  let calEvent = calAPI.getEventById("e" + event.id);
  if (calEvent) {
    calEvent.setProp("title", event.name);
    calEvent.setStart(event.start_date);
    calEvent.setEnd(event.end_date);
    calEvent.setExtendedProp("event", event);
  }
}
function eventDeleted(eventId) {
  let calEvent = calAPI.getEventById("e" + eventId);
  if (calEvent) calEvent.remove();
}

let availCreate = null;
let availUpdate = null;

function availInterfaces(interfaces) {
  availCreate = interfaces.newAvailability;
  availUpdate = interfaces.updateAvailability;
}

function availCreated({ avail, refresh }) {
  if (refresh) calAPI.refetchEvents();
  else calAPI.addEvent(availToCalEvent(avail), true);
}

function availUpdated(avail) {
  let calEvent = calAPI.getEventById("a" + avail.id);
  if (calEvent) {
    calEvent.setStart(avail.start_date);
    calEvent.setEnd(avail.end_date);
    calEvent.setExtendedProp("availability", avail);
    calEvent.setResources(avail.resources);
    calEvent.setProp("display", modeAvail.value ? "" : "background");
  }
}
function availDeleted(availId) {
  let calEvent = calAPI.getEventById("a" + availId);
  if (calEvent) calEvent.remove();
}

function selectTime(infos) {
  if (infos.resource.id == "event") {
    if (isAdmin.value) eventCreate(infos.startStr, infos.endStr);
  } else {
    if (modeAvail.value) {
      if (isAdmin.value)
      availCreate(infos.startStr, infos.endStr, infos.resource);
    } else {
      resaCreate(infos.startStr, infos.endStr, infos.resource);
    }
  }
}
function eventClick({ event }) {
  if ("event" in event.extendedProps) {
    if(isAdmin.value)eventUpdate(event.extendedProps["event"]);
  } else if ("resa" in event.extendedProps) {
    let resa = event.extendedProps["resa"];
    if(isAdmin.value || resa.own) resaUpdate(resa);
  } else if ("availability" in event.extendedProps) {
    if(isAdmin.value)availUpdate(event.extendedProps["availability"]);
  }
}
function refreshReservations() {
  store.dispatch("reservations/fetchList", datesQuery.value);
}
function changeMode() {
  modeAvail.value = !modeAvail.value;
}

const headerToolbar = {
  center: "resourceTimelineDay resourceTimelineWeek",
  left: "title",
  right: (isAdmin.value ? "availabilities " : "") + "refresh today prev,next",
};

const calendarOptions = {
  plugins: [resourceTimelinePlugin, interactionPlugin],
  schedulerLicenseKey: "GPL-My-Project-Is-Open-Source",
  initialView: "resourceTimelineWeek",
  locale: frLocale,
  height: "auto",
  contentHeight:"auto",
  aspectRatio: 0.5,
  selectable: true,
  weekends: false,
  initialDate: sessionStorage.getItem("start_date"),
  views: {
    resourceTimeline: {
      slotMinTime: import.meta.env.VITE_APP_START_HOUR,
      slotMaxTime: import.meta.env.VITE_APP_END_HOUR,
      slotDuration: "00:30:00",
      titleFormat: { year: "numeric", month: "2-digit", day: "2-digit" },
    },
  },

  customButtons: {
    refresh: {
      text: "Refresh",
      click: () => {
        store.dispatch("reservations/fetchList", datesQuery.value);
      },
    },
    availabilities: {
      text: "Availabilities",
      click: () => {
        modeAvail.value = true;
        headerToolbar.right = "reservations refresh today prev,next";
        calAPI.setOption("headerToolbar", headerToolbar);
        calAPI.refetchEvents();
      },
    },
    reservations: {
      text: "Reservations",
      click: () => {
        modeAvail.value = false;
        headerToolbar.right = "availabilities refresh today prev,next";
        calAPI.setOption("headerToolbar", headerToolbar);
        calAPI.refetchEvents();
      },
    },
  },
  headerToolbar: headerToolbar,
  resourceGroupField: "group",
  resourceOrder: "group",
  resources: [],

  select: selectTime,
  eventClick: eventClick,
  events: fetchCalEvents,
};
</script>
<style>
@import "@vueform/multiselect/themes/default.css";

.event-background {
  background: #007bff;
}
.avail-background {
  background: rgba(143, 223, 130, 0.3);
}
</style>
