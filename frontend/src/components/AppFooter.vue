<template>
  <footer>
    <div class="container-fluid mt-3 mb-3 border-top border-dark">
      <div class="row mt-3">
        <div class="col">
          <a class="logo-font" href="/"> FacManager </a>
          |
          <a class="logo-font" href="/legalnotice"> Legal notice </a>
        </div>
        <div class="col align-self-end media">
          <img
            :src="`${publicPath}logos-inp-uga.jpg`"
            width="30%"
            class="mr-4 float-end"
          />
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
const publicPath = import.meta.env.BASE_URL;
</script>
