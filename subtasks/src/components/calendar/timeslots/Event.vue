<template>
  <div class="event-container">
    <div class="event-header flex flex-col gap-0 px-2 pb-1 cursor-pointer">
      <div class="font-semibold leading-tight">
        {{ title || "New Event" }}
      </div>
      <div class="opacity-90 text-sm leading-tight">
        {{ timeRange }}
      </div>
    </div>
  </div>
</template>

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

/* Small: row layout, no padding */
@container event (max-height: 45px) {
  .event-header {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    padding-top: 0;
  }
}

/* Larger: add top padding */
@container event (min-height: 50px) {
  .event-header {
    padding-top: 4px;
  }
}
</style>

<script setup lang="ts">
defineProps<{
  title: string;
  timeRange: string;
}>();
</script>
