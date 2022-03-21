import createCrud from "./crud.factory";
import ApiService from "@/common/api.service";

const users_extra = {
  actions: {
    async create({ commit }, { data }) {
      const response = await ApiService.post("users/create_user", data)
      commit("createSuccess", response.data);
      return response.data;
    }
  }
}
const users = createCrud("users", users_extra);
export default users;
