<template>
  <Navbar solid>
    <template #default="{ isShowMenu }">
      <fwb-navbar-collapse :is-show-menu="isShowMenu">
        <RouterLink to="/projects">
          <p
            :class="active === 'projects' ? 'text-blue-700' : 'text-gray-700'"
            class="hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-blue-700 dark:text-gray-400 md:dark:hover:text-white dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent text-[17px]"
          >
            Projects
          </p>
        </RouterLink>
        <RouterLink to="/tasks">
          <p
            :class="active === 'tasks' ? 'text-blue-700' : 'text-gray-700'"
            class="hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-blue-700 dark:text-gray-400 md:dark:hover:text-white dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent text-[17px]"
          >
            Tasks
          </p>
        </RouterLink>
        <RouterLink to="/calendar">
          <p
            :class="active === 'calendar' ? 'text-blue-700' : 'text-gray-700'"
            class="hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-blue-700 dark:text-gray-400 md:dark:hover:text-white dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent text-[17px]"
          >
            Calendar
          </p>
        </RouterLink>
      </fwb-navbar-collapse>
    </template>
  </Navbar>
</template>

<script setup lang="ts">
import Navbar from "./shared/Navbar.vue";
import { FwbNavbarCollapse } from "flowbite-vue";
defineProps<{ active?: "projects" | "tasks" | "calendar" }>();
</script>
