<template>
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
import { ref, computed } from "vue";
import Multiselect from "@vueform/multiselect";

const emit = defineEmits(["update:modelValue"]);

const props = defineProps({
  resource: {
    type : Array,
    required: true,
  },
  modelValue: {
    type: Array,
    required: true,
  },
  create:{
    type: Function,
    default: ()=>{},
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

const options = computed(() =>
  props.resource.map((o) => {
    return { value: o.id, label: o.name };
  })
);

function addOption(query) {
    props.create({ name: query })
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
