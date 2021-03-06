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
import { requireAuth } from "./routeGards";

function requireManager(to, from, next) {
  if (store.getters.isAuthenticated) {
    var user = store.getters.authUser;
    if (
      user.entities.indexOf(parseInt(to.params["entityid"])) > -1 ||
      store.getters.isAdmin
    ) {
      next();
    } else {
      next("/");
    }
  }
}

export default {
  path: "/entities",
  component: () => import("../pages/entities/index.vue"),
  beforeEnter: requireAuth,
  meta: {
    breadcumb: {
      label: "Entités",
      name: "entitieslist",
    },
  },
  children: [
    {
      path: "",
      name: "entitieslist",
      component: () => import("../pages/entities/EntitiesList.vue"),
    },
    {
      path: ":entityid",
      component: () => import("../pages/entities/Entity.vue"),
      meta: {
        routeparam: "entityid",
        routedelete: "entities",
        breadcumb: {
          label: {
            ressource: "entities",
            labelprop: "name",
          },
          name: "entityinfos",
        },
      },
      children: [
        {
          path: "",
          name: "entityinfos",
          meta: {
            routeparam: "entityid",
            routedelete: "entities",
          },
          component: () => import("../pages/entities/EntityInfos.vue"),
        },
        {
          path: "edit",
          name: "entityedit",
          beforeEnter: requireManager,
          meta: {
            routeparam: "entityid",
            routedelete: "entities",
            breadcumb: {
              label: "Edit",
              name: "entityedit",
            },
          },
          component: () => import("../pages/entities/EntityEdit.vue"),
        },
        {
          path: "materials",
          beforeEnter: requireManager,
          meta: {
            breadcumb: {
              label: "Materiels",
              name: "materialslist",
            },
          },
          component: () => import("../pages/materials/Materials.vue"),
          children: [
            {
              path: "",
              name: "materialslist",
              component: () => import("../pages/materials/MaterialsList.vue"),
            },
            {
              path: "g/bulk",
              name: "genericmaterialbulk",
              component: () =>
                import("../pages/materials/GenericMaterialBulk.vue"),
              meta: {
                routeparam: "matid",
                routedelete: "materialslist",
                breadcumb: {
                  label: "Ajout Massif",
                  name: "genericmaterialbulk",
                },
              },
            },

            {
              path: "g/:matid",
              name: "genericmaterial",
              component: () =>
                import("../pages/materials/GenericMaterialEdit.vue"),
              meta: {
                routeparam: "matid",
                routedelete: "materialslist",
                breadcumb: {
                  label: {
                    ressource: "genericmaterials",
                    prefix: [
                      {
                        ressource: "entities",
                        param: "entityid",
                      },
                    ],
                    labelprop: "name",
                  },
                  name: "genericmaterial",
                },
              },
            },
            {
              path: "g/:matid/loans",
              name: "loansmaterialgeneric",
              component: () => import("../pages/entities/EntityLoansList.vue"),
              meta: {
                routeparam: "matid",
                breadcumb: {
                  label: {
                    ressource: "genericmaterials",
                    prefix: [
                      {
                        ressource: "entities",
                        param: "entityid",
                      },
                    ],
                    labelprop: "name",
                    labelchild: "Prêts",
                  },
                  name: "genericmaterial",
                },
              },
            },
            {
              path: "s/:matid",
              name: "specificmaterial",
              component: () =>
                import("../pages/materials/SpecificMaterialEdit.vue"),
              meta: {
                routeparam: "matid",
                routedelete: "materialslist",
                breadcumb: {
                  label: {
                    ressource: "specificmaterials",
                    prefix: [
                      {
                        ressource: "entities",
                        param: "entityid",
                      },
                    ],
                    labelprop: "name",
                  },
                  name: "specificmaterial",
                },
              },
            },
            {
              path: "s/:matid/loans",
              name: "loansmaterialspecific",
              component: () => import("../pages/entities/EntityLoansList.vue"),
              meta: {
                routeparam: "matid",
                breadcumb: {
                  label: {
                    ressource: "specificmaterials",
                    prefix: [
                      {
                        ressource: "entities",
                        param: "entityid",
                      },
                    ],
                    labelprop: "name",
                    labelchild: "Prêts",
                  },
                  name: "specificmaterial",
                },
              },
            },
          ],
        },
        {
          path: "loans",
          name: "entityloans",
          beforeEnter: requireManager,
          meta: {
            routeparam: "entityid",
            breadcumb: {
              label: "Prêts",
              name: "entityloans",
            },
          },
          component: () => import("../pages/entities/EntityLoansList.vue"),
        },
      ],
    },
  ],
};
