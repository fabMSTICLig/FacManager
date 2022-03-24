/*
 * Copyright (C) 2020-2022 LIG Université Grenoble Alpes
 *
 *
 * This file is part of FacManager.
 *
 * FacManager is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
 *
 * FacManager is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along with FacManager. If not, see <https://www.gnu.org/licenses/>
 *
 * @author Germain Lemasson
*/

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
