<!-- Component inspired from https://alligator.io/vuejs/vue-pagination-component/ -->
<template>
  <!--<nav v-if="!(isInFirstPage && isInLastPage) && totalPages != 0">-->
  <nav>
    <ul class="pagination">
      <li
        class="page-item"
        :class="{ disabled: isInFirstPage }"
      >
        <button
          class="page-link"
          aria-label="Go to first page"
          @click="onClickFirstPage"
        >
          First
        </button>
      </li>

      <li
        class="page-item"
        :class="{ disabled: isInFirstPage }"
      >
        <button
          class="page-link"
          aria-label="Go to previous page"
          @click="onClickPreviousPage"
        >
          Previous
        </button>
      </li>

      <li
        v-for="page in pages"
        :key="page.name"
        class="page-item"
        :class="{ active: isPageActive(page.name) }"
      >
        <button
          class="page-link"
          :aria-label="`Go to page number ${page.name}`"
          @click="onClickPage(page.name)"
        >
          {{ page.name }}
        </button>
      </li>

      <li
        class="page-item"
        :class="{ disabled: isInLastPage }"
      >
        <button
          class="page-link"
          aria-label="Go to next page"
          @click="onClickNextPage"
        >
          Next
        </button>
      </li>

      <li
        class="page-item"
        :class="{ disabled: isInLastPage }"
      >
        <button
          class="page-link"
          aria-label="Go to last page"
          @click="onClickLastPage"
        >
          Last
        </button>
      </li>
    </ul>
  </nav>
</template>
<script setup>
import { computed, defineProps, defineEmits } from "vue";
const props = defineProps({
  maxVisibleButtons: {
    type: Number,
    required: false,
    default: 3,
  },
  totalPages: {
    type: Number,
    required: true,
  },
  total: {
    type: Number,
    required: true,
  },
  perPage: {
    type: Number,
    required: true,
  },
  currentPage: {
    type: Number,
    required: true,
  },
});
const emit = defineEmits(["pagechanged"]);
const startPage = computed(() => {
  if (props.currentPage === 1) {
    return 1;
  }

  if (props.currentPage === props.totalPages) {
    return Math.max(props.totalPages - props.maxVisibleButtons + 1, 1);
  }

  return props.currentPage - 1;
});
const endPage = computed(() => {
  return Math.min(
    startPage.value + props.maxVisibleButtons - 1,
    props.totalPages
  );
});
const pages = computed(() => {
  const range = [];
  for (let i = startPage.value; i <= endPage.value; i += 1) {
    range.push({
      name: i,
      isDisabled: i === props.currentPage,
    });
  }

  return range;
});
const isInFirstPage = computed(() => {
  return props.currentPage <= 1;
});
const isInLastPage = computed(() => {
  return props.currentPage >= props.totalPages;
});
function onClickFirstPage() {
  emit("pagechanged", 1);
}
function onClickPreviousPage() {
  emit("pagechanged", props.currentPage - 1);
}
function onClickPage(page) {
  emit("pagechanged", page);
}
function onClickNextPage() {
  emit("pagechanged", props.currentPage + 1);
}
function onClickLastPage() {
  emit("pagechanged", props.totalPages);
}
function isPageActive(page) {
  return props.currentPage === page;
}
</script>
