<template>
  <Navbar solid>
    <template #default="{ isShowMenu }">
      <fwb-navbar-collapse :is-show-menu="isShowMenu">
        <fwb-navbar-link is-active link="#">
          <p class="text-[17px]">Projects</p>
        </fwb-navbar-link>
        <fwb-navbar-link link="#">
          <p class="text-[17px]">Tasks</p>
        </fwb-navbar-link>
        <fwb-navbar-link link="#">
          <p class="text-[17px]">Calendar</p>
        </fwb-navbar-link>
      </fwb-navbar-collapse>
    </template>
  </Navbar>
</template>

<script setup lang="ts">
import Navbar from "./shared/Navbar.vue";
import { FwbNavbarCollapse, FwbNavbarLink } from "flowbite-vue";
</script>
