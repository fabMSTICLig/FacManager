import { watch } from "vue";

export default function useSearchStorage(
  name,
  fetch,
  defaults,
  currentPage,
  perPage
) {
  function ssGetOrDefault(key, defaultValue) {
    return sessionStorage.getItem(key)
      ? JSON.parse(sessionStorage.getItem(key))
      : defaultValue;
  }

  function setWatch(key, theref) {
    watch(theref, () => {
      sessionStorage.setItem(name + "_" + key, JSON.stringify(theref.value));
    });
  }

  let refsList = [];
  let resetValues = {};

  for (const [key] of Object.entries(defaults)) {
    resetValues[key] = defaults[key].value;
    if ("_set" in defaults[key])
      defaults[key]._set(
        ssGetOrDefault(name + "_" + key, defaults[key].value),
        true
      );
    else
      defaults[key].value = ssGetOrDefault(
        name + "_" + key,
        defaults[key].value
      );
    setWatch(key, defaults[key]);
    refsList.push(defaults[key]);
  }

  function resetSearch() {
    for (const [key] of Object.entries(defaults)) {
      if ("_set" in defaults[key]) defaults[key]._set(resetValues[key], true);
      else defaults[key].value = resetValues[key];
    }
  }

  async function refresh() {
    let params = {};
    for (const [key] of Object.entries(defaults)) {
      if (defaults[key].value) params[key] = defaults[key].value;
    }
    if (!isNaN(perPage)) {
      params["limit"] = perPage;
      params["offset"] = (currentPage.value - 1) * perPage;
    }
    await fetch(params);
  }
  if (currentPage) {
    currentPage.value = ssGetOrDefault(name + "_page", 1);
    watch(currentPage, () => {
      sessionStorage.setItem(name + "_page", JSON.stringify(currentPage.value));
      refresh();
    });
    watch(refsList, () => {
      currentPage.value = 1;
      refresh();
    });
  }

  return { refresh, resetSearch };
}
