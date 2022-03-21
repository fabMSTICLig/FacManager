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
