<template>
  <ul class="list-group list-group-horizontal d-flew flex-wrap">
    <li
      v-for="item in items"
      :key="item"
      class="list-group-item border rounded"
    >
      {{ item[fieldName] }}
    </li>
  </ul>
</template>

<script setup>
defineProps({
  items: {
    type: Array,
    required: true,
  },
  fieldName: {
    type: String,
    required: false,
    default: "name",
  },
});
</script>
