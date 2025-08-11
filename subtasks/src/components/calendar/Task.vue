<template>
  <div class="h-full bg-green-500 py-2 px-3 pointer-events-none">
    <div class="flex flex-row mb-1 items-center gap-1">
      <span class="pi-check-circle pi text-xs" />
      <div class="font-semibold text-ellipsis truncate">{{ title || "New Task" }}</div>
    </div>
    <div class="opacity-90 text-sm">{{ timeEstimateDisplay }}</div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";

const props = defineProps<{
  title: string;
  timeEstimate: number;
}>();

const timeEstimateDisplay = computed(() => {
  const hours = Math.floor(props.timeEstimate / 60);
  const mins = props.timeEstimate % 60;
  if (hours) {
    return `${hours}h ${mins}M`;
  }
  return `${mins}M`;
});
</script>
