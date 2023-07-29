<template>
  <div>
    <div v-if="!readonly">
      <div class="input-group" style="height: 43px">
        <Multiselect
          ref="mtselect"
          :model-value="valuesIntern"
          track-by="id"
          label="name"
          mode="multiple"
          :options="fetchOptions"
          :loading="optionsLoading"
          :clear-on-select="true"
          :close-on-select="true"
          :filter-results="false"
          :resolve-on-load="true"
          :delay="200"
          :searchable="true"
          :multiple-label="multipleLabel"
          no-options-text="Veuillez entrer des charactères"
          :can-clear="false"
          open-direction="top"
          @select="select"
        />
      </div>
    </div>
    <ul class="list-group">
      <li
        v-for="item in valuesIntern"
        :key="item.id"
        class="list-group-item d-flex justify-content-between align-items-center"
      >
        <span>
          <slot :item="item">
            <strong>@{{ item.username }} :</strong>
            {{ item.first_name }}
            {{ item.last_name }}
          </slot>
        </span>
        <button
          v-if="!readonly"
          class="btn btn-danger"
          type="button"
          @click="removeItem(item)"
        >
          X
        </button>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useUsersStore } from "@/stores/users";

import Multiselect from "@vueform/multiselect";

const emit = defineEmits(["update:modelValue"]);

const props = defineProps({
  modelValue: {
    type: Array,
    required: true,
  },
  readonly: {
    type: Boolean,
    required: false,
    default: false,
  },
});

const usersStore = useUsersStore();

const mtselect = ref();
const valuesIntern = ref([]);
const optionsLoading = ref(false);
onMounted(async () => {
  valuesIntern.value = await usersStore.fetchList({
    ids: props.modelValue.join(","),
  });
});

function multipleLabel() {
  return "";
}

async function fetchOptions(query) {
  let data = [];
  if (query) {
    optionsLoading.value = true;
    data = await usersStore.fetchList({ search: query });
    optionsLoading.value = false;
  }
  return data
    .filter((o) => !valuesIntern.value.some((v) => v.id == o.id))
    .map((o) => {
      return {
        name: "@" + o.username + " " + o.first_name + " " + o.last_name,
        value: o,
        disabled: false,
      };
    });
}

function select(o) {
  valuesIntern.value.push(o);
  emit(
    "update:modelValue",
    valuesIntern.value.map((o) => o.id)
  );
}
function removeItem(item) {
  let index = valuesIntern.value.findIndex((o) => o.id == item.id);
  if (index != -1) valuesIntern.value.splice(index, 1);
  emit(
    "update:modelValue",
    valuesIntern.value.map((o) => o.id)
  );
}
</script>
<style src="@vueform/multiselect/themes/default.css"></style>
