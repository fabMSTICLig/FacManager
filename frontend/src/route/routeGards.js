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

import store from "../store";

export async function requireAuth(to, from, next) {
  if (!store.getters.isAuthenticated) {
    try{
    await store.dispatch("checkAuth");
    } catch(e)
    {}
  }
  if (store.getters.isAuthenticated) {
    if (
      to.name == "profile" ||
      (store.getters.authUser.first_name &&
        store.getters.authUser.last_name &&
        store.getters.authUser.email &&
        store.getters.authUser.rgpd_accept)
    ) {
      next();
    } else {
      next({
        name: "profile",
      });
    }
  } else {
    next("/");
  }
}
export async function requireAdmin(to, from, next) {
  if (!store.getters.isAuthenticated) {
    await store.dispatch("checkAuth");
  }
  if (store.getters.isAuthenticated && store.getters.isAdmin) {
    next();
  } else {
    next({
      name: "home",
    });
  }
}
