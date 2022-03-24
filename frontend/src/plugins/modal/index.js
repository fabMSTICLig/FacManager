/*
 * Copyright (C) 2020-2022 LIG Université Grenoble Alpes
 *
 *
 * This file is part of FacManager.
 *
 * FacManager is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
 *
 * FacManager is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along with FacManager. If not, see <https://www.gnu.org/licenses/>
 *
 * @author Germain Lemasson
*/

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
