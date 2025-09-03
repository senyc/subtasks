<template>
  <div class="event-container bg-green-600">
    <div class="event-header flex flex-col gap-0 px-2 pb-1 pointer-events-none">
      <div class="flex flex-row items-center gap-1">
        <span class="pi-check-circle pi" />
        <div class="font-semibold text-ellipsis truncate">
          {{ title || "New Task" }}
        </div>
      </div>
      <div class="opacity-90 text-sm">{{ timeEstimateDisplay }}</div>
    </div>
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
    if (mins) {
      return `${hours}h ${mins}m`;
    }
    return `${hours}h`;
  }
  return `${mins}m`;
});
</script>

<style>
.event-container {
  container-type: size;
  container-name: event;
  height: 100%;
}

.event-header {
  /* Default: column layout */
  display: flex;
  flex-direction: column;
}

@container event (max-height: 45px) {
  .event-header {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    padding-top: 0;
  }
}

@container event (min-height: 50px) {
  .event-header {
    padding-top: 4px;
  }
}
</style>
