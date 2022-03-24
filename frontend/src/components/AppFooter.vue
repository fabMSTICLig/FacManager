<!--
Copyright (C) 2020-2022 LIG Université Grenoble Alpes


This file is part of FacManager.

FacManager is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

FacManager is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with FacManager. If not, see <https://www.gnu.org/licenses/>

@author Germain Lemasson
-->

<template>
  <footer>
    <div class="container-fluid mt-3 mb-3 border-top border-dark">
      <div class="row mt-3">
        <div class="col">
          <a class="logo-font" href="/"> FacManager </a>
          |
            <router-link
              :to="{ name: 'legalnotice' }"
            >
              Legal notice
            </router-link>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
const publicPath = import.meta.env.BASE_URL;
</script>
