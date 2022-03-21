import { createRouter, createWebHashHistory } from "vue-router";
import { requireAdmin, requireAuth } from "./routeGards";

const routes = [
  {
    path: "/",
    name: "home",
    component: () => import("../pages/Home.vue"),
  },
  {
    path: "/profile",
    name: "profile",
    beforeEnter: requireAuth,
    component: () => import("../pages/profile/Profile.vue"),
  },
  {
    path: "/myusages",
    name: "myusages",
    beforeEnter: requireAuth,
    component: () => import("../pages/faccore/usages/UsagesList.vue"),
  },
  {
    path: "/reservations",
    name: "reservations",
    beforeEnter: requireAuth,
    component: () => import("../pages/reservations/Reservations.vue"),
  },
  {
    path: "/usages",
    name: "usages",
    beforeEnter: requireAdmin,
    component: () => import("../pages/faccore/usages/UsagesList.vue"),
  },
  {
    path: "/organizations",
    component: () =>
      import("../pages/facusers/organizations/Organizations.vue"),
    beforeEnter: requireAdmin,
    meta: {
      breadcumb: {
        label: "Organizations",
        name: "organizations",
      },
    },
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
          breadcumb: {
            label: {
              ressource: "organizations",
              labelprop: "name",
            },
            name: "organization",
          },
        },
        component: () =>
          import("../pages/facusers/organizations/OrganizationEdit.vue"),
      },
    ],
  },
  {
    path: "/projects",
    component: () => import("../pages/facusers/projects/Projects.vue"),
    beforeEnter: requireAdmin,
    meta: {
      breadcumb: {
        label: "Projects",
        name: "projects",
      },
    },
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
          breadcumb: {
            label: {
              ressource: "projects",
              labelprop: "name",
            },
            name: "projectedit",
          },
        },
        component: () => import("../pages/facusers/projects/Project.vue"),
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
              breadcumb: {
                label: "Usages",
                name: "projectusages",
              },
            },
            component: () => import("../pages/faccore/usages/UsagesList.vue"),
          },
        ],
      },
    ],
  },
  {
    path: "/users",
    component: () => import("../pages/facusers/users/Users.vue"),
    beforeEnter: requireAdmin,
    meta: {
      breadcumb: {
        label: "Utilisateurs",
        name: "users",
      },
    },
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
          breadcumb: {
            label: {
              ressource: "users",
              labelprop: "username",
            },
            name: "useredit",
          },
        },
        component: () => import("../pages/facusers/users/User.vue"),
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
              breadcumb: {
                label: "Usages",
                name: "userusages",
              },
            },
            component: () => import("../pages/faccore/usages/UsagesList.vue"),
          },
        ],
      },
    ],
  },
  {
    path: "/managers",
    component: () => import("../pages/faccore/managers/Managers.vue"),
    beforeEnter: requireAdmin,
    meta: {
      breadcumb: {
        label: "Managers",
        name: "managers",
      },
    },
    children: [
      {
        path: "",
        name: "managers",
        component: () => import("../pages/faccore/managers/ManagersList.vue"),
      },
      {
        path: ":managerid",
        name: "manager",
        meta: {
          routeparam: "managerid",
          routedelete: "managers",
          breadcumb: {
            label: {
              ressource: "managers",
              labelprop: "name",
            },
            name: "manager",
          },
        },
        component: () => import("../pages/faccore/managers/ManagerEdit.vue"),
      },
    ],
  },
  {
    path: "/machines",
    component: () => import("../pages/faccore/machines/Machines.vue"),
    beforeEnter: requireAdmin,
    meta: {
      breadcumb: {
        label: "Machines",
        name: "machines",
      },
    },
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
          breadcumb: {
            label: {
              ressource: "machine_models",
              labelprop: "name",
            },
            name: "machine",
          },
        },
        component: () => import("../pages/faccore/machines/MachineEdit.vue"),
      },
    ],
  },
  {
    path: "/supplies",
    component: () => import("../pages/faccore/supplies/Supplies.vue"),
    beforeEnter: requireAdmin,
    meta: {
      breadcumb: {
        label: "Supplies",
        name: "supplies",
      },
    },
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
          breadcumb: {
            label: {
              ressource: "supplies",
              labelprop: "name",
            },
            name: "supply",
          },
        },
        component: () => import("../pages/faccore/supplies/SupplyEdit.vue"),
      },
    ],
  },
  {
    path: "/resatypes",
    component: () => import("../pages/faccore/resatypes/ReservationTypes.vue"),
    beforeEnter: requireAdmin,
    meta: {
      breadcumb: {
        label: "Reservation Types",
        name: "resatypes",
      },
    },
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
          breadcumb: {
            label: {
              ressource: "reservation_types",
              labelprop: "name",
            },
            name: "resatype",
          },
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
