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

import { createRouter, createWebHashHistory, RouterView } from "vue-router";
import { requireAdmin, requireAuth } from "./routeGards";
const routes = [
  {
    path: "/",
    name: "home",
    component: () => import("../pages/HomeApp.vue"),
  },
  {
    path: "/legalnotice",
    name: "legalnotice",
    component: () => import("../pages/LegalNotice.vue"),
  },

  {
    path: "/profile",
    name: "profile",
    beforeEnter: requireAuth,
    component: () => import("../pages/profile/MyProfile.vue"),
  },
  {
    path: "/myusages",
    name: "myusages",
    beforeEnter: requireAuth,
    component: () => import("../pages/faccore/usages/UsagesList.vue"),
  },
  {
    path: "/reservations/:resaid?",
    name: "reservations",
    beforeEnter: requireAuth,
    props: true,
    component: () => import("../pages/reservations/ReservationsView.vue"),
  },
  {
    path: "/usages",
    name: "usages",
    beforeEnter: requireAdmin,
    component: () => import("../pages/faccore/usages/UsagesList.vue"),
  },
  {
    path: "/organizations",
    component: RouterView,
    beforeEnter: requireAdmin,
    children: [
      {
        path: "",
        name: "organizations",
        component: () =>
          import("../pages/facusers/organizations/OrganizationsList.vue"),
      },
      {
        path: ":orgaid",
        name: "organization",
        meta: {
          routeparam: "orgaid",
          routedelete: "organizations",
        },
        component: () =>
          import("../pages/facusers/organizations/OrganizationEdit.vue"),
      },
    ],
  },
  {
    path: "/projects",
    component: RouterView,
    beforeEnter: requireAdmin,
    children: [
      {
        path: "",
        name: "projects",
        component: () => import("../pages/facusers/projects/ProjectsList.vue"),
      },
      {
        path: ":projectid",
        name: "project",
        meta: {
          routeparam: "projectid",
          routedelete: "projects",
        },
    component: RouterView,
        children: [
          {
            path: "edit",
            name: "projectedit",
            meta: {
              routeparam: "projectid",
              routedelete: "projects",
            },
            component: () =>
              import("../pages/facusers/projects/ProjectEdit.vue"),
          },
          {
            path: "usages",
            name: "projectusages",
            meta: {
              routeparam: "projectid",
            },
            component: () => import("../pages/faccore/usages/UsagesList.vue"),
          },
        ],
      },
    ],
  },
  {
    path: "/users",
    component: RouterView,
    beforeEnter: requireAdmin,
    children: [
      {
        path: "",
        name: "users",
        component: () => import("../pages/facusers/users/UsersList.vue"),
      },
      {
        path: ":userid",
        name: "user",
        meta: {
          routeparam: "userid",
          routedelete: "users",
        },
    component: RouterView,
        children: [
          {
            path: "edit",
            name: "useredit",
            meta: {
              routeparam: "userid",
              routedelete: "users",
            },
            component: () =>
              import("../pages/facusers/users/UserEdit.vue"),
          },
          {
            path: "usages",
            name: "userusages",
            meta: {
              routeparam: "userid",
            },
            component: () => import("../pages/faccore/usages/UsagesList.vue"),
          },
        ],
      },
    ],
  },
  {
    path: "/machines",
    component: RouterView,
    beforeEnter: requireAdmin,
    children: [
      {
        path: "",
        name: "machines",
        component: () => import("../pages/faccore/machines/MachinesList.vue"),
      },
      {
        path: ":machineid",
        name: "machine",
        meta: {
          routeparam: "machineid",
          routedelete: "machines",
        },
        component: () => import("../pages/faccore/machines/MachineEdit.vue"),
      },
    ],
  },
  {
    path: "/supplies",
    component: RouterView,
    beforeEnter: requireAdmin,
    children: [
      {
        path: "",
        name: "supplies",
        component: () => import("../pages/faccore/supplies/SuppliesList.vue"),
      },
      {
        path: ":supplyid",
        name: "supply",
        meta: {
          routeparam: "supplyid",
          routedelete: "supplies",
        },
        component: () => import("../pages/faccore/supplies/SupplyEdit.vue"),
      },
    ],
  },
  {
    path: "/resatypes",
    component: RouterView,
    beforeEnter: requireAdmin,
    children: [
      {
        path: "",
        name: "resatypes",
        component: () =>
          import("../pages/faccore/resatypes/ReservationTypesList.vue"),
      },
      {
        path: ":resatypeid",
        name: "resatype",
        meta: {
          routeparam: "resatypeid",
          routedelete: "resatypes",
        },
        component: () =>
          import("../pages/faccore/resatypes/ReservationTypeEdit.vue"),
      },
    ],
  },
];
const router = createRouter({
  history: createWebHashHistory(),
  routes, // short for `routes: routes`
});

export default router;
