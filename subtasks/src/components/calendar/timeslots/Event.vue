<template>
  <div class="py-2 px-3 pointer-events-none">
    <div class="font-semibold mb-1">{{ title || "New Event" }}</div>
    <div class="opacity-90 text-sm">{{ timeRange }}</div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  title: string;
  timeRange: string;
}>();
</script>
