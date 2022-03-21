<template>
  <div id="projects">
    <Breadcumb />
    <router-view />
  </div>
</template>

<script setup>
import Breadcumb from "@/components/nav/AppBreadcumb.vue";
</script>
