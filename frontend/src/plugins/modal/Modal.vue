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
          <div v-if="!hideHeader" class="modal-header">
            <h5 class="modal-title">
              {{ title }}
            </h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
              @click.prevent="handleClose()"
            ></button>
          </div>
          <div class="modal-body">
            <slot>
              <p>{{ content }}</p>
            </slot>
          </div>
          <div v-if="!hideFooter" class="modal-footer">
            <button
              v-if="!confirmFooter"
              type="button"
              class="btn btn-primary"
              @click.prevent="handleClose()"
            >
              Ok
            </button>
            <button
              v-if="confirmFooter"
              type="button"
              class="btn btn-primary"
              @click.prevent="handleConfirm()"
            >
              Oui
            </button>
            <button
              v-if="confirmFooter"
              type="button"
              class="btn btn-danger"
              @click.prevent="handleReject()"
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
    resolve: {
      type: Function,
    },
  },
  setup(props) {
    function handleClose() {
      if (props.resolve) {
        props.resolve(null);
      }
    }

    function handleConfirm() {
      if (props.resolve) {
        props.resolve(true);
      }
    }

    function handleReject() {
      if (props.resolve) {
        props.resolve(false);
      }
    }

    return {
      handleClose,
      handleConfirm,
      handleReject,
    };
  },
};
export default Modal;
</script>
