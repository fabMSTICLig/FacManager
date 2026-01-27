<!--
Copyright (C) 2020-2022 LIG Université Grenoble Alpes


This file is part of FacManager.

FacManager is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

FacManager is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with FacManager. If not, see <https://www.gnu.org/licenses/>

@author Germain Lemasson
-->

<template>
  <div class="home">
    <div class="row justify-content-center">
      <div class="col-12 col-md-12">
        <HomeTop />
      </div>
      <div class="col col-12">
        <div
          v-if="loaded"
          class="card mt-2"
        >
          <div class="card-header">
            <h2>Planning</h2>
          </div>
          <div class="card-body">
            <div>
              <FullCalendar
                ref="calendar"
                :options="calendarOptions"
              />
            </div>
            <div>Les machines n'apparaissant pas sont libres.</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
/*
 */
import FullCalendar from "@fullcalendar/vue3";
import resourceTimelinePlugin from "@fullcalendar/resource-timeline";
import frLocale from "@fullcalendar/core/locales/fr";
import bootstrap5Plugin from "@fullcalendar/bootstrap5";

import { ref, onBeforeMount, nextTick } from "vue";
import { useRouter } from "vue-router";
import { storeToRefs } from "pinia";
import { useMachinesStore } from "@/stores/machines";
import { useMachineModelsStore } from "@/stores/machines";
import {
  useReservationTypesStore,
  useReservationsStore,
} from "@/stores/reservations";
import { useManagersStore } from "@/stores/managers";
import { useEventsStore } from "@/stores/events";
import { useResourcesStore } from "@/stores/resources";

import HomeTop from "@/pages/HomeTop.vue";

const router = useRouter();

const calendar = ref();
const loaded = ref(false);
const resources = ref([]);
const datesQuery = ref({});

let busyColor = "#dc3545";

const reservationsStore = useReservationsStore();
const { list: reservations } = storeToRefs(reservationsStore);
const reservationTypesStore = useReservationTypesStore();
const { objects: reservationTypes } = storeToRefs(reservationTypesStore);
const machineModelsStore = useMachineModelsStore();
const { list: machine_models } = storeToRefs(machineModelsStore);
const eventsStore = useEventsStore();
const { list: events } = storeToRefs(eventsStore);
const managersStore = useManagersStore();
const { list: managers } = storeToRefs(managersStore);

let calAPI = null;
onBeforeMount(async () => {
  const resStore = useResourcesStore();
  const { businessHours, minHour, maxHour } = storeToRefs(resStore);
  await resStore.fetchResources();
  calendarOptions.views.resourceTimeline.slotMinTime = minHour.value;
  calendarOptions.views.resourceTimeline.slotMaxTime = maxHour.value;
  calendarOptions.businessHours = businessHours.value;
  resources.value.push({
    id: "event",
    title: "Events",
    group: "01 Events",
    businessHours: {
      startTime: minHour.value,
      endTime: maxHour.value,
    },
  });
  resources.value = resources.value.concat(
    managers.value.map((manager) => {
      return {
        id: "m" + manager.id,
        title: manager.name,
        group: "02 Managers",
        manager: manager,
        businessHours: manager.businessHours,
      };
    }),
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

  loaded.value = true;
  await nextTick();
  calAPI = calendar.value.getApi();
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
    color: busyColor,
    own: resa.own,
    resourceIds: [],
    resa: resa,
  };
  if (resa.machine) calEvent.resourceIds.push(resa.machine);
  if (resa.manager) calEvent.resourceIds.push("m" + resa.manager);
  if (resa.own) calEvent.borderColor = "red";
  return calEvent;
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
  ]).then(() => {
    let ev = [];
    ev = reservations.value.map(resaToCalEvent);
    ev = ev.concat(events.value.map(eventToCalEvent));
    ev = ev.concat(
      managers.value.map((manager) => {
        return {
          title: manager.name,
          start: dateInfo.startStr,
          end: dateInfo.startStr,
          id: manager.name,
          resourceIds: ["m" + manager.id],
        };
      }),
    );
    success(ev);
  });
}
const calendarOptions = {
  plugins: [bootstrap5Plugin, resourceTimelinePlugin],
  schedulerLicenseKey: "GPL-My-Project-Is-Open-Source",
  initialView: "resourceTimelineWeek",
  locale: frLocale,
  height: "auto",
  contentHeight: "auto",
  weekends: false,
  selectConstraint: "businessHours",
  filterResourcesWithEvents: true,
  themeSystem: "bootstrap5",
  resourceGroupField: "group",
  resourceOrder: "group",
  resources: [],
  views: {
    resourceTimeline: {
      slotMinTime: "00:00",
      slotMaxTime: "23:59",
      slotDuration: "02:00:00",
      titleFormat: { year: "numeric", month: "2-digit", day: "2-digit" },
    },
  },
  customButtons: {
    prevWeek: {
      text: "<",
      click: function () {
        calAPI.incrementDate({ days: -7 });
      },
    },
    nextWeek: {
      text: ">",
      click: function () {
        calAPI.incrementDate({ days: 7 });
      },
    },
    reservation: {
      text: "Réservation",
      click: function () {
        router.push("reservations");
      },
    },
  },
  headerToolbar: {
    left: "title",
    right: "reservation today prevWeek,nextWeek",
  },
  events: fetchCalEvents,
};
</script>
