import ApiService from "../common/api.service";

function mergeDeep(...objects) {
  const isObject = (obj) => obj && typeof obj === "object";

  return objects.reduce((prev, obj) => {
    Object.keys(obj).forEach((key) => {
      const pVal = prev[key];
      const oVal = obj[key];

      if (Array.isArray(pVal) && Array.isArray(oVal)) {
        prev[key] = pVal.concat(...oVal);
      } else if (isObject(pVal) && isObject(oVal)) {
        prev[key] = mergeDeep(pVal, oVal);
      } else {
        prev[key] = oVal;
      }
    });

    return prev;
  }, {});
}

/*
  Création d'un objet commun pour les appels CRUD
  Fusionne un store global avec les ascendents 
*/
const createCrud = (ressource, source) => {
  const target = {
    namespaced: true,

    state: {
      entities: {},
      count: 0,
    },
    getters: {
      list(state) {
        return Object.values(state.entities)
      },
      byId(state) {
        return (id) => {
          return (id ? state.entities[id.toString()] : null);
        }
      },
    },
    actions: {
      async fetchList({ commit, getters }, { prefix = "", params = {} } = {}) {
        const { data } = await ApiService.query(prefix + ressource, params);
        commit("fetchListSuccess", data);
        return getters.list;
      },
      async fetchSingle({ commit, state }, { id, prefix = "" }) {
        if(Object.keys(state.entities).indexOf(id)>-1) return state.entities[id]

        const { data } = await ApiService.get(prefix + ressource, id);
        commit("fetchSingleSuccess", data);
        return data;
      },
      async create({ commit }, { data, prefix = "" }) {
        const response = await ApiService.post(prefix + ressource, data);
        commit("createSuccess", response.data);
        return response.data;
      },
      async update({ commit }, { id, data, prefix = "" }) {
        const response = await ApiService.update(prefix + ressource, id, data);
        commit("updateSuccess", response.data);
        return response.data;
      },
      async destroy({ commit }, { id, prefix = "" }) {
        const { data } = await ApiService.delete(prefix + ressource, id);
        commit("destroySuccess", id);
        return data;
      },
    },

    mutations: {
      fetchListSuccess(state, data) {
        let entities = {};
        data.results.forEach((m) => {
          entities[m["id"].toString()] = m;
        });
        state.entities = entities;
        state.count = data.count;
      },
      fetchSingleSuccess(state, data) {
        const id = data["id"].toString();
        state.entities = { ...state.entities, [id]: data };
      },
      createSuccess(state, data) {
        if (data) {
          const id = data["id"].toString();
          state.entities = { ...state.entities, [id]: data };
        }
      },
      updateSuccess(state, data) {
        if (data["id"]) {
          const id = data["id"].toString();
          state.entities = { ...state.entities, [id]: data };
        }
      },
      destroySuccess(state, id) {
        delete state.entities[id.toString()];
      },
    },
  };
  return mergeDeep(target, source);
};
export default createCrud;
