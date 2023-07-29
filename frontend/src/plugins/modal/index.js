import { createVNode, render } from "vue";
import Modal from "./Modal.vue";

Modal.install = function (app) {
  const confirmHandler = async (options) => {
    let node = null;
    const container = document.createElement("div");

    const response = await new Promise((resolve) => {
      const localOptions = {
        show: true,
        hideHeader: true,
        confirmFooter: true,
      };
      const vm = createVNode(Modal, {
        ...localOptions,
        ...options,
        resolve,
      });
      render(vm, container);

      node = container.firstElementChild;
      document.body.appendChild(node);
    });

    document.querySelector("body").removeChild(node);

    return response;
  };

  app.provide("confirm", confirmHandler);

  const showHandler = async (options) => {
    let node = null;
    const container = document.createElement("div");

    const response = await new Promise((resolve) => {
      const localOptions = {
        show: true,
        hideHeader: true,
        confirmFooter: false,
      };
      const vm = createVNode(Modal, {
        ...options,
        ...localOptions,
        resolve,
      });
      render(vm, container);

      node = container.firstElementChild;
      document.body.appendChild(node);
    });

    document.querySelector("body").removeChild(node);

    return response;
  };
  app.provide("show", showHandler);
};

export default Modal;
