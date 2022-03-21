<template>
  <div>
    <div v-if="!readonly">
      <div
        class="input-group"
        style="height: 43px"
      >
        <Multiselect
          ref="mtselect"
          :model-value="valuesIntern"
          track-by="id"
          label="name"
          mode="multiple"
          :options="fetchOptions"
          :loaing="optionsLoading"
          :clear-on-select="!isArray"
          :close-on-select="!isArray"
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
            {{ item.name }}
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
import { ref, computed, onMounted, defineProps, defineEmits } from "vue";
import { useStore } from "vuex";

import Multiselect from "@vueform/multiselect";

const store = useStore();

const emit = defineEmits(["update:modelValue"]);

const props = defineProps({
  ressource: {
    type: [String, Array],
    required: true,
  },
  modelValue: {
    type: Array,
    required: true,
  },
  makeLabel: {
    type: Function,
    default: (o) => o.name,
  },
  readonly: {
    type: Boolean,
    required: false,
    default: false,
  },
});

const mtselect = ref();
const valuesIntern = ref([]);
const optionsLoading = ref(false);
const isArray = computed(() => Array.isArray(props.ressource));
onMounted(async () => {
  if (!isArray.value) {
    valuesIntern.value = await store.dispatch(props.ressource + "/fetchList", {
      params: { ids: props.modelValue.join(",") },
    });
  } else {
    valuesIntern.value = props.ressource.filter((o) =>
      props.modelValue.includes(o.id)
    );
  }
});

function multipleLabel() {
  return "";
}

async function fetchOptions(query) {
  let data = [];
  if (Array.isArray(props.ressource)) {
    if (query == null) query = "";
    data = props.ressource.filter((o) => o.name.includes(query));
  } else {
    if (query) {
      optionsLoading.value = true;
      data = await store.dispatch(props.ressource + "/fetchList", {
        params: { search: query },
      });
      optionsLoading.value = false;
    }
  }
  return data
    .filter((o) => !valuesIntern.value.some((v) => v.id == o.id))
    .map((o) => {
      return {
        name: props.makeLabel(o),
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
  if(isArray.value) mtselect.value.refreshOptions();
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
