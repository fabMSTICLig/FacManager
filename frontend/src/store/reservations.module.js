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
