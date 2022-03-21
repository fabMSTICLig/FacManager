<template>
  <!--  <ul class="list-group list-group-horizontal d-flew flex-wrap">
    <li
      v-for="item in objects_filtered"
      :key="item.id"
      class="list-group-item border rounded"
    >
      <span> {{ item.name }}</span>
      <button
        type="button"
        class="btn btn-danger btn-sm ml-1"
        @click="removeTag(item)"
      >
        X
      </button>
    </li>
    <input
      v-model="inputValue"
      type="text"
      class="form-control"
      :list="_uid"
      placeholder="Add"
      @keyup.enter="addTag"
      @change="addTag"
    >
    <datalist
      v-if="activeDset"
      :id="_uid"
    >
      <option
        v-for="item in objects_datalist"
        :key="item.id"
        :value="item.name"
        v-text="item.name"
      />
    </datalist>
  </ul>-->
  <Multiselect
    ref="input"
    :model-value="modelValue"
    mode="tags"
    :close-on-select="false"
    :searchable="true"
    :create-option="!forbidAdd"
    :append-new-option="false"
    :append-new-tag="false"
    :options="options"
    @option="addOption"
    @deselect="removeOption"
    @change="change"
  />
</template>
<script setup>
import { ref, computed, onBeforeMount, defineProps, defineEmits } from "vue";
import { useStore } from "vuex";
import Multiselect from "@vueform/multiselect";

const emit = defineEmits(["update:modelValue"]);

const props = defineProps({
  ressource: {
    type: String,
    required: true,
  },
  modelValue: {
    type: Array,
    required: true,
  },
  forbidAdd: {
    type: Boolean,
    default: false,
  },
  noLoad: {
    type: Boolean,
    default: false,
  },

});

const input = ref();

const store = useStore();
onBeforeMount(() => {
  if(!props.noLoad)store.dispatch(props.ressource + "/fetchList",{params:{limit:1000}});
});

const options = computed(() =>
  store.getters[props.ressource + "/list"].map((o) => {
    return { value: o.id, label: o.name };
  })
);

function addOption(query) {
  store
    .dispatch(props.ressource + "/create", {
      data: { name: query },
    })
    .then((data) => {
      emit("update:modelValue", [].concat(props.modelValue).concat([data.id]));
    })
    .catch((error) => {
      console.log(JSON.stringify(error));
    });
}

function removeOption(option) {
  emit(
    "update:modelValue",
    props.modelValue.filter((v) => v != option)
  );
}

function change(v) {
  emit("update:modelValue", v.filter(e=>typeof e === 'number'));
}
</script>
<style src="@vueform/multiselect/themes/default.css"></style>
