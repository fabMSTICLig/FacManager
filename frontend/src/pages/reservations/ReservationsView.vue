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
        <div class="d-flex text-light">
          <span class="event-background p-2">Event</span>
          <span
            v-for="(v, k) in RESA_COLORS"
            :key="k"
            class="fc-event p-2"
            :style="'background-color:' + v"
            v-text="'Reservation ' + k"
          ></span>
          <span class="p-2 text-dark" style="border: 1px solid red"
            >My reservations</span
          >
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
    <modal
      id="modal-charter"
      title="Charter"
      :show="showCharter"
      :resolve="() => (showCharter = false)"
    >
      <p>
        You must read the charter before you can make any reservation.
        <a :href="charterUrl">{{ charterUrl }}</a>
      </p>
    </modal>
  </div>
</template>

<script setup>
import FullCalendar from "@fullcalendar/vue3";
import resourceTimelinePlugin from "@fullcalendar/resource-timeline";
import frLocale from "@fullcalendar/core/locales/fr";
import interactionPlugin from "@fullcalendar/interaction";
import bootstrap5Plugin from '@fullcalendar/bootstrap5';

import { ref, nextTick, onBeforeMount } from "vue";
import { storeToRefs } from "pinia";
import { useAuthStore } from "@/stores/auth";
import { useTrainingLevelsStore } from "@/stores/traininglevels";
import { useResourcesStore } from "@/stores/resources";
import { useMachineModelsStore } from "@/stores/machines";
import {
  useReservationTypesStore,
  useReservationsStore,
} from "@/stores/reservations";
import { useManagersStore } from "@/stores/managers";
import { useEventsStore } from "@/stores/events";

import ReservationEdit from "./ReservationEdit.vue";
import EventEdit from "./EventEdit.vue";
import Modal from "@/plugins/modal";

const authStore = useAuthStore();
const { authUser, isAdmin } = storeToRefs(authStore);
const trainingLevelsStore = useTrainingLevelsStore();

const RESA_COLORS = JSON.parse(import.meta.env.VITE_APP_RESA_COLORS);

const loaded = ref(false);
const calendar = ref();
let calAPI = null;

const props = defineProps({
  resaid: {
    type: String,
    required: false,
    default: null,
  },
});


const showCharter = ref(false);
const charterUrl = import.meta.env.VITE_APP_CHARTER_URL;

const resources = ref([]);
const datesQuery = ref({});

const reservationsStore = useReservationsStore();
const { list: reservations } = storeToRefs(reservationsStore);
const reservationTypesStore = useReservationTypesStore();
const { objects: reservationTypes } = storeToRefs(reservationTypesStore);
const machineModelsStore = useMachineModelsStore();
const { list: machine_models } = storeToRefs(machineModelsStore);
const eventsStore = useEventsStore();
const { list: events } = storeToRefs(eventsStore);
const managersStore = useManagersStore();
const { list: managers, events:managersEvents } = storeToRefs(managersStore);


onBeforeMount(async () => {
  const resStore = useResourcesStore();
  const {businessHours, minHour, maxHour} = storeToRefs(resStore)
  await resStore.fetchResources();
  calendarOptions.views.resourceTimeline.slotMinTime=minHour.value;
  calendarOptions.views.resourceTimeline.slotMaxTime=maxHour.value;
  calendarOptions.businessHours=businessHours.value;
  resources.value.push({ id: "event", title: "Events", group: "01 Events" });
  resources.value = resources.value.concat(
    managers.value.map((manager) => {
      return {
        id: "m"+manager.id,
        title: manager.name,
        group: "02 Managers",
        manager: manager,
      };
    })
  );
  machine_models.value.forEach((mm) => {
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
  let resa = null;
  if(props.resaid)
  {
    resa = await reservationsStore.fetchSingle(props.resaid)
  }
  await trainingLevelsStore.fetchList({}, "/users/" + authUser.value.id + "/");
  loaded.value = true;
  await nextTick();
  calAPI = calendar.value.getApi();
  if(resa)
  {
    calAPI.gotoDate(resa.start_date)
    if (isAdmin.value || resa.own) resaUpdate(resa);
  }
  if (!authUser.value.charter) showCharter.value = true;

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
      reservationTypes.value[resa.reservation_type].name + "\n" + resa.status,
    start: resa.start_date,
    end: resa.end_date,
    id: resa.id,
    color: RESA_COLORS[resa.status],
    own: resa.own,
    resourceIds: [],
    resa: resa,
  };
  if (resa.machine) calEvent.resourceIds.push(resa.machine);
  if (resa.manager) calEvent.resourceIds.push("m"+resa.manager);
  if (resa.own) calEvent.borderColor = "red";
  return calEvent;
}

function managerEventToCalEvent(event) {
  return {
    title: "",
    start: event.dtstart,
    end: event.dtend,
    id: "me" + event.id,
    display: 'background',
    color: "red",
    resourceId: "m"+event.manager,
  };
}
function fetchCalEvents(dateInfo, success) {
  datesQuery.value = {
    mindate: dateInfo.startStr,
    maxdate: dateInfo.endStr,
  };
  sessionStorage.setItem("start_date", dateInfo.startStr);
  Promise.all([
    reservationsStore.fetchList(datesQuery.value),
    eventsStore.fetchList(datesQuery.value),
    managersStore.fetchEvents(datesQuery.value),
  ]).then(() => {
    let ev = [];
    ev = reservations.value.map(resaToCalEvent);
    ev = ev.concat(events.value.map(eventToCalEvent));
    ev = ev.concat(managersEvents.value.map(managerEventToCalEvent));
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
  if (Array.isArray(resa))
  {
    for(var i = 0;i <resa.length;i++){
      calAPI.addEvent(resaToCalEvent(resa[i]), true);
    }
  }
  else
  {
    calAPI.addEvent(resaToCalEvent(resa), true);
  }
}

function resaUpdated(resa) {
  let calEvent = calAPI.getEventById(resa.id);
  if (calEvent) {
    calEvent.setProp(
      "title",
      reservationTypes.value[resa.reservation_type].name + "\n" + resa.status
    );
    calEvent.setStart(resa.start_date);
    calEvent.setEnd(resa.end_date);
    calEvent.setExtendedProp("resa", resa);
    calEvent.setProp("color", RESA_COLORS[resa.status]);
    calEvent.setExtendedProp("own", resa.own);
    if (resa.own) calEvent.setProp("borderColor", "red");
    let resids = [];
    if (resa.machine) resids.push(resa.machine);
    if (resa.manager) resids.push("m"+resa.manager);
    calEvent.setResources(resids);
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
  if (Array.isArray(event))
  {
    for(var i = 0;i <event.length;i++){
      calAPI.addEvent(eventToCalEvent(event[i]), true);
    }
  }
  else
  {
  calAPI.addEvent(eventToCalEvent(event), true);
  }
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
function selectTime(infos) {
  if (infos.resource.id == "event") {
    if (isAdmin.value) eventCreate(infos.startStr, infos.endStr);
  } else {
    resaCreate(infos.startStr, infos.endStr, infos.resource);
  }
}
function eventClick({ event }) {
  if ("event" in event.extendedProps) {
    if (isAdmin.value) eventUpdate(event.extendedProps["event"]);
  } else if ("resa" in event.extendedProps) {
    let resa = event.extendedProps["resa"];
    if (isAdmin.value || resa.own) resaUpdate(resa);
  }
}

const headerToolbar = {
  center: "resourceTimelineDay resourceTimelineWeek",
  left: "title",
  right: "refresh today prevWeek,nextWeek",
};



const calendarOptions = {
  plugins: [bootstrap5Plugin, resourceTimelinePlugin, interactionPlugin],
  schedulerLicenseKey: "GPL-My-Project-Is-Open-Source",
  initialView: "resourceTimelineWeek",
  themeSystem: 'bootstrap5',
  locale: frLocale,
  height: "auto",
  contentHeight: "auto",
  aspectRatio: 0.5,
  selectable: true,
  selectConstraint: "businessHours",
  weekends: false,
  initialDate: sessionStorage.getItem("start_date"),
  views: {
    resourceTimeline: {
      slotMinTime: '00:00',
      slotMaxTime: '23:59',
      slotDuration: "00:30:00",
      titleFormat: { year: "numeric", month: "2-digit", day: "2-digit" },
    },
  },

  customButtons: {
    refresh: {
      text: "Refresh",
      click: () => {
        reservationsStore.fetchList(datesQuery.value);
      },
    },
    prevWeek: {
      text : "<",
      click: function() {
            calAPI.incrementDate( { days: -7 } );
          }
    },
    nextWeek: {
      text : ">",
      click: function() {
            calAPI.incrementDate( { days: 7 } );
          }
    }
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
</style>
