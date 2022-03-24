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

import createCrud from "./crud.factory";

const resa_extra = {
  mutations: {
    createSuccess(state, data) {
        if (data) {
          const id = data["id"].toString();
          state.entities = { ...state.entities, [id]: data };
          if(data['user']==this.getters["authUser"].id)
          {
            this.getters["authUser"].reservations.push(id)
          }
        }
    },
  }
};

export const reservation_types = createCrud("reservation_types", {});
export const reservations = createCrud("reservations", resa_extra);
