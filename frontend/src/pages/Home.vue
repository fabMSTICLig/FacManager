<template>
  <div class="home">
    <div class="row justify-content-center">
      <div class="col-12 col-md-12">
        <div class="card">
          <div class="card-header">
            <h1>Site de reservation du FabMSTIC</h1>
          </div>
          <div class="card-body">
            <p>
              Ce site permet aux utilisateurs du FabMSTIC de réserver des
              créneaux horraires.
            </p>
            <p>Les étapes à suivre pour la première réservation:</p>
            <ul>
              <li>
                Se connecter au site en utilisant le
                <a href="accounts/login?next=/">CAS UGA</a>
              </li>
              <li>
                Remplir les informations de son
                <router-link :to="{ name: 'profile' }">profil</router-link>
                (nom, prénom, email)
              </li>
              <li>
                Lire la
                <a href="https://fabmstic.imag.fr/pages/la-charte.html"
                  >charte</a
                >
              </li>
              <li>Attendre que votre compte soit validé</li>
              <li>
                Réserver un crénaux en choisissant une Initiation (Laser, 3D,
                ...)
              </li>
              <li>
                Attendre le mail confirmant que votre réservation est acceptée
              </li>
            </ul>
          </div>
        </div>
      </div>
      <div class="col col-12">
        <div class="card mt-2" v-if="loaded">
          <div class="card-header">
            <h2>Planning</h2>
          </div>
          <div class="card-body">
            <div>
              <FullCalendar :options="calendarOptions" ref="calendar"/>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
/*
*/
import "@fullcalendar/core/vdom"; // solves problem with Vite
import FullCalendar from "@fullcalendar/vue3";
import frLocale from "@fullcalendar/core/locales/fr";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import { nextTick,ref,onBeforeMount } from "vue";

import { useStore } from "vuex";
const store = useStore();

const RESA_COLORS = JSON.parse(import.meta.env.VITE_APP_RESA_COLORS);

const calendar = ref();
const loaded = ref(false);
const datesQuery = ref({});
const calEventsLoading = ref(false);
let calAPI = null;

onBeforeMount(async () => {
  await store.dispatch("resources/fetchResources",{min:true});
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
  };
}
function fetchCalEvents(dateInfo, success, failure) {
  datesQuery.value = {
    mindate: dateInfo.startStr,
    maxdate: dateInfo.endStr,
  };
  Promise.all([
    store.dispatch("reservations/fetchList", { params: datesQuery.value }),
    store.dispatch("events/fetchList", { params: datesQuery.value }),
  ]).then(() => {
    let ev = [];
    store.getters["reservations/list"].forEach((resa) => {
      resa.uses.forEach((machine) => {
        ev.push({
          title: store.getters["machines/byId"](machine).name,
          start: resa.start_date,
          end: resa.end_date,
          id: resa.id + "" + machine,
          color: RESA_COLORS[resa.status],
        });
      });
      if (resa.manager) {
        ev.push({
          title: store.getters["managers/byId"](resa.manager).name,
          start: resa.start_date,
          end: resa.end_date,
          id: "m" + resa.id + "" + resa.manager,
          color: RESA_COLORS[resa.status],
        });
      }
    });
    ev = ev.concat(store.getters["events/list"].map(eventToCalEvent));
    success(ev);
  });
}
const calendarOptions = {
  plugins: [timeGridPlugin],
  initialView: "timeGridWeek",
  locale: frLocale,
  height: "auto",
  weekends: false,
  views: {
    timeGridWeek: {
      type: "timeGrid",
      slotMinTime: import.meta.env.VITE_APP_START_HOUR,
      slotMaxTime: import.meta.env.VITE_APP_END_HOUR,
      allDaySlot: false,
      titleFormat: { year: "numeric", month: "2-digit", day: "2-digit" },
    },
  },
  events: fetchCalEvents,
};
</script>
