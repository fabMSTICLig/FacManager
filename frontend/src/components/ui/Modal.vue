<!--
Copyright (C) 2020-2022 LIG Université Grenoble Alpes


This file is part of FacManager.

FacManager is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

FacManager is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with FacManager. If not, see <https://www.gnu.org/licenses/>

@author Germain Lemasson
-->

<template>
  <div v-if="show">
    <div class="modal-backdrop show" />
    <div
      class="modal"
      :class="{ show: show }"
      :style="{ display: show ? 'block' : 'none' }"
      tabindex="-1"
      role="dialog"
    >
      <div class="modal-dialog modal-dialog-scrollable">
        <div class="modal-content">
          <div
            v-if="!hideHeader"
            class="modal-header"
          >
            <h5 class="modal-title">
              {{ title }}
            </h5>
            <button
              type="button"
              class="close"
              data-dismiss="modal"
              aria-label="Close"
              @click="close"
            >
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <slot>
              <p>{{ content }}</p>
            </slot>
          </div>
          <div
            v-if="!hideFooter"
            class="modal-footer"
          >
            <button
              v-if="!confirmFooter"
              type="button"
              class="btn btn-primary"
              @click.prevent="close"
            >
              Ok
            </button>
            <button
              v-if="confirmFooter"
              type="button"
              class="btn btn-primary"
              @click.prevent="confirm(true)"
            >
              Oui
            </button>
            <button
              v-if="confirmFooter"
              type="button"
              class="btn btn-danger"
              @click.prevent="confirm(false)"
            >
              Non
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export const Modal = {
  name: "modal",
  props: {
    content: {
      type: null,
      default: "",
    },
    hideHeader: {
      type: Boolean,
      default: false,
    },
    hideFooter: {
      type: Boolean,
      default: false,
    },
    title: {
      type: String,
      default: "Title",
    },
    show: {
      type: Boolean,
      default: false,
    },
    confirmFooter: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    close() {
      this.$emit("close");
    },
    confirm(val) {
      this.$emit("confirm", val);
    },
  },
};
export default Modal;
</script>
