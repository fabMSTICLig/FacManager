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
