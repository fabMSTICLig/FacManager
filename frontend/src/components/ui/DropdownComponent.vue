<template>
  <div
    ref="root"
    class="btn-group"
    :class="{ 'nav-item': isNav }"
    role="group"
    @focusout="hide"
  >
    <a
      :id="'button' + uid"
      href=""
      class="dropdown-toggle"
      :class="[isNav ? 'nav-link' : 'btn '+btnStyle, { show: show }]"
      data-bs-toggle="dropdown"
      aria-expanded="false"
      @click.prevent="toogle"
      >{{ label }}</a
    >
    <ul :id="'tooltip' + uid" class="dropdown-menu" :class="{ show: show }" :style="show ? style : ''">
      <li v-for="item in items" :key="item.label">
        <router-link v-slot="{ href, navigate }" :to="item.to" custom>
          <a
            :href="href"
            class="dropdown-item"
            @click="goto($event, navigate)"
            >{{ item.label }}</a
          >
        </router-link>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { v4 as uuidv4 } from "uuid";

defineProps({
  items: {
    type: Array,
    required: true,
  },
  label: {
    type: String,
    required: true,
  },
  isNav: {
    type: Boolean,
    required: false,
    default: false,
  },
  btnStyle: {
    type: String,
    default: 'btn-primary',
  }
});
const uid = uuidv4();
const show = ref(false);

const style="position: absolute; inset: 0px auto auto 0px; margin: 0px; transform: translate(0px, 40px);"

const toogle = function () {
  show.value = !show.value;
};
const root = ref(null);
function hide(e) {
  if (root.value && !root.value.contains(e.relatedTarget)) {
    show.value = false;
  }
}
const goto = function (event, navigate) {
  show.value = false;
  navigate(event);
};
</script>
