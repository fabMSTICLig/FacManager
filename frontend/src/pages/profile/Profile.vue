<!--
Copyright (C) 2020-2022 LIG Université Grenoble Alpes


This file is part of FacManager.

FacManager is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

FacManager is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with FacManager. If not, see <https://www.gnu.org/licenses/>

@author Germain Lemasson
-->

<template>
  <div class="card">
    <div class="card-header">
      <h3>Votre profile</h3>
    </div>
    <div class="card-body">
      <form id="editor-form" class="form">
        <div class="mb-3">
          <label class="form-label" for="username">Username</label
          ><input
            id="username"
            v-model="authUser.username"
            class="form-control"
            type="text"
            readonly
          />
        </div>
        <div class="mb-3">
          <label class="form-label" for="firstname">First name</label
          ><input
            id="firstname"
            v-model="authUser.first_name"
            class="form-control"
            type="text"
            required
            :readonly="extern"
          />
        </div>
        <div class="mb-3">
          <label class="form-label" for="lastname">Last name</label
          ><input
            id="lastname"
            v-model="authUser.last_name"
            class="form-control"
            type="text"
            required
            :readonly="extern"
          />
        </div>
        <div class="mb-3">
          <label class="form-label" for="email">Email</label
          ><input
            id="email"
            v-model="authUser.email"
            class="form-control"
            type="email"
            required
            :readonly="extern"
          />
        </div>
        <template v-if="!authUser.externe">
          <div class="mb-3">
            <label for="oldPassword">Old password:</label>
            <div v-if="goodpassword" class="valid-feedback d-block">
              Password changed
            </div>
            <div v-if="goodpassword == false" class="invalid-feedback d-block">
              Wrong Password
            </div>

            <div v-if="passvalid == false" class="invalid-feedback d-block">
              The old password is required for changing it
            </div>
            <div v-if="passvalid == false" class="invalid-feedback d-block">
              The new password is required
            </div>
            <div v-if="passvalid == false" class="invalid-feedback d-block">
              The Confirm Password is required and must be the same as New
              Password
            </div>

            <input
              id="oldPassword"
              v-model="oldPassword"
              class="form-control"
              type="password"
              :class="
                passvalid == null ? '' : passvalid ? 'is-valid' : 'is-invalid'
              "
              placeholder="Enter current password"
            />
          </div>
          <div class="mb-3">
            <label for="newpass">New password:</label>
            <input
              id="newpass"
              v-model="newPassword"
              class="form-control"
              type="password"
              :class="
                passvalid == null ? '' : passvalid ? 'is-valid' : 'is-invalid'
              "
              placeholder="Enter new password"
            />
          </div>
          <div class="mb-3">
            <label for="newpassconf">Confirm new password:</label>
            <input
              id="newpassconf"
              v-model="newPasswordConf"
              class="form-control"
              type="password"
              :class="
                passvalid == null ? '' : passvalid ? 'is-valid' : 'is-invalid'
              "
              placeholder="Confirm password"
            />
          </div>
        </template>

        <div v-if="authUser.rgpd_accept" class="mb-3">
          <label class="form-label">Organizations</label>
          <DynList v-model="authUser.organizations" ressource="organizations" />
        </div>
        <div class="mt-2" role="group">
          <button class="btn btn-primary" type="button" @click="updateUser">
            Update
          </button>
        </div>
      </form>
    </div>
    <modal id="modal-rgpd" v-model:show="showRGPD" title="RGPD" hide-footer>
      <h6>Conditions d'utilisation</h6>
      <p>
        Pour permettre le bon fonctionnment du site certaines de vos
        informations sont stockées.
      </p>
      <p>
        Name d'utilisateur, Prénom, Name, Email sont utilisés afin de vous
        contacter. Seul les managers des entités ont accés à ces informations.
      </p>
      <p>
        Ces informations ainsi que celles liées aux prêts seront stockées 3 ans
        après que vous ayez quitté l'université ou sur demande à l'adresse
        matos@univ-grenoble-alpes.fr
      </p>

      <h6>Accepter vous ces termes ?</h6>
      <div>
        <div class="btn-group" role="group" aria-label="RGPD Accept">
          <button type="button" class="btn btn-primary" @click="acceptRGPD">
            Oui
          </button>
          <button
            type="button"
            class="btn btn-danger"
            @click="showRGPD = false"
          >
            Non
          </button>
        </div>
      </div>
    </modal>
  </div>
</template>
<script setup>
import { ref, computed, inject, onBeforeMount } from "vue";
import { useStore } from "vuex";

import DynList from "@/components/ui/DynList.vue";
import Modal from "@/plugins/modal";

const store = useStore();
const showModal = inject("show");

const authUser = computed(() => store.getters.authUser);
const extern = computed(() => store.getters.authUser.extern);
const showRGPD = ref(false);
function acceptRGPD() {
  store.dispatch("updateRGPD").then(() => {
    showRGPD.value = false;
    store.dispatch("organizations/fetchList");
  });
}

onBeforeMount(() => {
  if (!authUser.value.rgpd_accept) {
    showRGPD.value = true;
  }
});

async function updateUser() {
  if (passvalid.value != false) {
    await store.dispatch("updateAuthUser", authUser.value);
    if (oldPassword.value != "") {
      try {
        await store.dispatch("updatePassword", {
          old_password: oldPassword.value,
          new_password: newPassword.value,
        });
        goodpassword.value = true;
        showModal({ content: "Profile mis à jour" });
      } catch (e) {
        if (e.response.status == 400) {
          goodpassword.value = false;
        }
        console.log(e.response);
      }
    }
  }
}

const oldPassword = ref();
const newPassword = ref();
const newPasswordConf = ref();

const goodpassword = ref(null);
const passvalid = computed(() => {
  if (
    oldPassword.value == "" &&
    newPassword.value == "" &&
    newPasswordConf.value == ""
  )
    return null;
  if (
    (oldPassword.value != "" && newPassword.value == "") ||
    (oldPassword.value == "" && newPassword.value != "") ||
    (newPassword.value == "" && newPasswordConf.value == "")
  )
    return false;
  if (newPassword.value != newPasswordConf.value) return false;

  return true;
});
</script>
