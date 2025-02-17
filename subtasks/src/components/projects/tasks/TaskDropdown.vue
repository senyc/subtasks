<template>
  <fwb-dropdown placement="left" text="Left" close-inside>
    <template #trigger>
      <fwb-button color="light">
        <svg class="w-5 h-5" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 4 15">
          <path
            d="M3.5 1.5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0Zm0 6.041a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0Zm0 5.959a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0Z" />
        </svg>
      </fwb-button>
    </template>
    <nav class="p-2 hover:bg-gray-200 text-lg text-gray-700 text-nowrap">
      <RouterLink :to="`/projects/${projectId}/tasks/completed`">Show completed</RouterLink>
    </nav>
  </fwb-dropdown>
</template>

<script setup lang='ts'>
import { FwbDropdown } from 'flowbite-vue'

defineProps<{
  projectId: number
}>()

</script>
