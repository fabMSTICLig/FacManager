import { createStore } from "vuex";

import auth from "./auth.module";
import { reservations, reservation_types } from "./reservations.module";
import resources from "./resources.module";
import events from "./events.module";
import managers from "./managers.module";
import { machines } from "./machines.module";
// Create a new store instance.
const store = createStore({
  modules: {
    auth,
    resources,
    reservations,
    reservation_types,
    events,
    managers,
    machines
  },
});

export default store;
