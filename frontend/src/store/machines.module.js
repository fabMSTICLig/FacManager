import createCrud from "./crud.factory";

export const machines = createCrud("machines", {});
export const machine_models = createCrud("machine_models", {});
