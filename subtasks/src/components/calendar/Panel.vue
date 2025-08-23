<template>
  <div class="h-full flex flex-col">
    <div
      class="grid grid-cols-1 relative grid-rows-23 flex-grow mt-1"
      @mousedown="startCreateTimeSlot"
      @mousemove="updateTempTimeSlot"
      @mouseup="finishCreatingTimeSlot"
    >
      <div
        class="border-t border-t-black/20"
        v-for="hour in 23"
        :key="hour"
        :data-hour="hour"
      ></div>

      <div
        v-if="isCreating && previewTimeSlot"
        class="absolute left-1 right-1 bg-blue-500/50 border-2 border-blue-500 border-dashed rounded pointer-events-none z-10"
        :style="{
          top: `calc((${previewTimeSlot.startMinutes} / ${ONE_DAY}) * 100%)`,
          height: `calc((${previewTimeSlot.duration} / ${ONE_DAY}) * 100%)`,
        }"
      >
        <div class="p-2 text-white text-sm">
          <div>New Event</div>
          <div class="text-xs opacity-90">{{ previewTimeSlot.timeRange }}</div>
        </div>
        <TimeSlot
          :full-screen="true"
          v-if="tempTimeSlot"
          :timeSlot="tempTimeSlot"
        />
      </div>
    </div>
  </div>

  <NewTimeSlot
    @create-time-slot="createTimeSlot"
    @cancel-time-slot="cancelTimeSlot"
    v-model:timeSlot="tempTimeSlot!"
    v-model:visible="visible"
  />
</template>
<script setup lang="ts">
import { ref, computed } from "vue";
import NewTimeSlot from "./timeslots/NewTimeSlot.vue";
import type { TimeSlotForm } from "@annotations/models/timeSlot";
import TimeSlot from "./timeslots/TimeSlot.vue";

const visible = ref(false);

const props = defineProps<{
  date: Date;
}>();

// Sync query data to local state once fetched
const emit = defineEmits<{
  createTimeSlot: [timeSlot: TimeSlotForm];
}>();

const tempTimeSlot = ref<TimeSlotForm>();

// Event creation state
const isCreating = ref(false);
const createStartY = ref(0);
const createCurrentY = ref(0);
const createStartMinutes = ref(0);

const ONE_DAY = 1440;
const SNAP_INTERVAL_MINUTES = 15;
const MINIMUM_TIME_SLOT_DURATION_MINUTES = 60;

function createTimeSlot(event: TimeSlotForm) {
  tempTimeSlot.value = undefined;
  emit("createTimeSlot", event);
}

function cancelTimeSlot() {
  tempTimeSlot.value = undefined;
}

// Convert mouse position to minutes from midnight
const getMinutesFromMouseY = (
  mouseY: number,
  containerElement: HTMLElement,
) => {
  const rect = containerElement.getBoundingClientRect();
  const relativeY = mouseY - rect.top;
  const percentage = relativeY / rect.height;
  const minutes = Math.max(0, Math.min(ONE_DAY, percentage * ONE_DAY));

  return Math.round(minutes / SNAP_INTERVAL_MINUTES) * SNAP_INTERVAL_MINUTES;
};

const formatTime = (minutesFromMidnight: number) => {
  const date = new Date();
  date.setHours(0, 0, 0, 0);
  date.setMinutes(minutesFromMidnight);
  return date.toLocaleTimeString([], {
    hour: "numeric",
    minute: "2-digit",
    hour12: true,
  });
};

const previewTimeSlot = computed(() => {
  const startMinutes = Math.min(createStartMinutes.value, createCurrentY.value);
  const endMinutes = Math.max(createStartMinutes.value, createCurrentY.value);
  const duration = Math.max(SNAP_INTERVAL_MINUTES, endMinutes - startMinutes);

  return {
    startMinutes,
    duration,
    timeRange: `${formatTime(startMinutes)} - ${formatTime(startMinutes + duration)}`,
  };
});

const startCreateTimeSlot = (e: MouseEvent) => {
  e.preventDefault();
  const container = e.currentTarget as HTMLElement;
  const minutes = getMinutesFromMouseY(e.clientY, container);

  isCreating.value = true;
  createStartY.value = e.clientY;
  createCurrentY.value = minutes;
  createStartMinutes.value = minutes;

  // Prevent text selection during drag
  document.body.style.userSelect = "none";
};

const updateTempTimeSlot = (e: MouseEvent) => {
  if (!isCreating.value) return;

  e.preventDefault();
  const container = e.currentTarget as HTMLElement;
  createCurrentY.value = getMinutesFromMouseY(e.clientY, container);
};

const finishCreatingTimeSlot = (e: MouseEvent) => {
  if (!isCreating.value) return;
  e.preventDefault();

  const startMinutes = Math.min(createStartMinutes.value, createCurrentY.value);
  const endMinutes = Math.max(createStartMinutes.value, createCurrentY.value);
  const duration = Math.max(
    MINIMUM_TIME_SLOT_DURATION_MINUTES,
    endMinutes - startMinutes,
  );

  // Only create if surpasses minimum size
  if (duration >= SNAP_INTERVAL_MINUTES) {
    const startTime = new Date(props.date);
    startTime.setHours(0, startMinutes, 0, 0);

    const endTime = new Date(startTime);
    endTime.setMinutes(endTime.getMinutes() + duration);

    const newTimeSlot: TimeSlotForm = {
      start_at: startTime.toISOString(),
      end_at: endTime.toISOString(),
      title: "New Event",
      is_recurring: false,
      type: "event",
    };

    tempTimeSlot.value = newTimeSlot;
    visible.value = true;
  }

  isCreating.value = false;
  createStartY.value = 0;
  createCurrentY.value = 0;
  createStartMinutes.value = 0;
  document.body.style.userSelect = "";
};
</script>
