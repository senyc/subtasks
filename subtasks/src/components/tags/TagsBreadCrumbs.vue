<template>
  <section class="h-12 flex flex-row items-center">
    <fwb-breadcrumb>
      <fwb-breadcrumb-item home href="/">
        <template #home-icon>
          <div />
        </template>
        <RouterLink
          class="text-gray-700 hover:text-gray-900 dark:hover:text-white text-[17px]"
          to="/"
        >
          Subtasks
        </RouterLink>
      </fwb-breadcrumb-item>
      <fwb-breadcrumb-item class="text-xl">
        <template #arrow-icon>
          <svg
            class="mr-1 size-7 text-gray-400"
            fill="currentColor"
            viewBox="0 0 20 20"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              clip-rule="evenodd"
              d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
              fill-rule="evenodd"
            />
          </svg>
        </template>
        <RouterLink
          class="text-gray-700 hover:text-gray-900 dark:hover:text-white text-[17px]"
          to="/tasks"
        >
          Tasks
        </RouterLink>
      </fwb-breadcrumb-item>
      <fwb-breadcrumb-item class="text-xl" href="#">
        <template #arrow-icon>
          <svg
            class="mr-1 size-7 text-gray-400"
            fill="currentColor"
            viewBox="0 0 20 20"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              clip-rule="evenodd"
              d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
              fill-rule="evenodd"
            />
          </svg>
        </template>
        <p class="text-[17px]">Tags</p>
      </fwb-breadcrumb-item>
    </fwb-breadcrumb>
    <div class="flex gap-5 items-center ml-auto">
      <div><TagModalToggle /></div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { FwbBreadcrumb, FwbBreadcrumbItem } from "flowbite-vue";

import TagModalToggle from "./TagModalToggle.vue";

</script>
