<template>
  <div class="">
    <h3
      class="font-bold text-xl"
      :class="{
        'bg-blue-500 inline-flex flex-row items-center justify-center px-2 rounded-full text-white':
          date?.toDateString() == new Date().toDateString(),
        'text-center': cardView,
      }"
    >
      {{ date?.getDate() }}
    </h3>
    <div
      v-if="!cardView"
      class="relative grid grid-cols-1 grid-rows-23 h-full mt-1"
      @mousedown="startCreateEvent"
      @mousemove="updateCreateEvent"
      @mouseup="finishCreateEvent"
    >
      <!-- Hour grid lines -->
      <div
        class="border-t border-t-black/20 h-3"
        v-for="hour in 23"
        :key="hour"
        :data-hour="hour"
      ></div>

      <Event
        v-for="event in allEvents"
        :key="'id' in event ? event.id : 'new'"
        :event="event"
      />

      <!-- Preview event while dragging -->
      <div
        v-if="isCreating && previewEvent"
        class="absolute left-1 right-1 bg-blue-500/50 border-2 border-blue-500 border-dashed rounded pointer-events-none z-10"
        :style="{
          top: `calc((${previewEvent.startMinutes} / 1440) * 100%)`,
          height: `calc((${previewEvent.duration} / 1440) * 100%)`,
        }"
      >
        <div class="p-2 text-white text-sm">
          <div>New Event</div>
          <div class="text-xs opacity-90">{{ previewEvent.timeRange }}</div>
        </div>
      </div>
    </div>
  </div>

  <NewTimeSlot
    @create-time-slot="createTimeSlot"
    @cancel-time-slot="cancelTimeSlot"
    v-model:timeSlot="tempEvent!"
    v-model:visible="visible"
  />
</template>

<script setup lang="ts">
import Event from "./Event.vue";
import { ref, computed } from "vue";
import NewTimeSlot from "./events/NewTimeSlot.vue";
import type {
  TimeSlotForm,
  TimeSlotResponse,
} from "@annotations/models/timeSlot";

const visible = ref(false);

const props = withDefaults(
  defineProps<{
    date: Date;
    cardView?: boolean;
    events?: TimeSlotResponse[];
  }>(),
  {
    cardView: false,
  },
);

const tempEvent = ref<TimeSlotForm>();

function cancelTimeSlot() {
  tempEvent.value = undefined;
}

function createTimeSlot(event: TimeSlotForm) {
  tempEvent.value = undefined;
  emit("createTimeSlot", event);
}

const allEvents = computed<(TimeSlotForm | TimeSlotResponse)[]>(() =>
  tempEvent.value
    ? [...(props.events ?? []), tempEvent.value]
    : [...(props.events ?? [])],
);

// Sync query data to local state once fetched
const emit = defineEmits<{
  createTimeSlot: [event: TimeSlotForm];
}>();

// Event creation state
const isCreating = ref(false);
const createStartY = ref(0);
const createCurrentY = ref(0);
const createStartMinutes = ref(0);

// Convert mouse position to minutes from midnight
const getMinutesFromMouseY = (
  mouseY: number,
  containerElement: HTMLElement,
) => {
  const rect = containerElement.getBoundingClientRect();
  const relativeY = mouseY - rect.top;
  const percentage = relativeY / rect.height;
  const minutes = Math.max(0, Math.min(1440, percentage * 1440)); // 1440 minutes in day

  // Snap to 15-minute intervals
  return Math.round(minutes / 15) * 15;
};

const formatTime = (minutes: number) => {
  const hours = Math.floor(minutes / 60);
  const mins = minutes % 60;
  const period = hours >= 12 ? "PM" : "AM";
  const displayHour = hours > 12 ? hours - 12 : hours === 0 ? 12 : hours;
  const displayMinutes = mins.toString().padStart(2, "0");
  return `${displayHour}:${displayMinutes} ${period}`;
};

// Preview event data
const previewEvent = computed(() => {
  if (!isCreating.value) return null;

  const startMinutes = Math.min(createStartMinutes.value, createCurrentY.value);
  const endMinutes = Math.max(createStartMinutes.value, createCurrentY.value);
  const duration = Math.max(15, endMinutes - startMinutes); // Minimum 15 minutes

  return {
    startMinutes,
    duration,
    timeRange: `${formatTime(startMinutes)} - ${formatTime(startMinutes + duration)}`,
  };
});

const startCreateEvent = (e: MouseEvent) => {
  // Only start creating if clicking on empty space (not on existing events)
  if ((e.target as HTMLElement).closest(".event-box")) return;

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

const updateCreateEvent = (e: MouseEvent) => {
  if (!isCreating.value) return;

  e.preventDefault();
  const container = e.currentTarget as HTMLElement;
  createCurrentY.value = getMinutesFromMouseY(e.clientY, container);
};

const finishCreateEvent = (e: MouseEvent) => {
  if (!isCreating.value) return;

  e.preventDefault();

  const startMinutes = Math.min(createStartMinutes.value, createCurrentY.value);
  const endMinutes = Math.max(createStartMinutes.value, createCurrentY.value);
  const duration = Math.max(60, endMinutes - startMinutes); // Minimum 1 hour

  // Create the new event
  if (duration >= 15) {
    // Only create if dragged for at least 15 minutes
    const startTime = new Date(props.date);
    startTime.setHours(0, startMinutes, 0, 0);

    const endTime = new Date(startTime);
    endTime.setMinutes(endTime.getMinutes() + duration);

    const newEvent: TimeSlotForm = {
      start_at: startTime.toISOString(),
      end_at: endTime.toISOString(),
      title: "New Event",
      is_recurring: false,
      type: "event",
    };

    tempEvent.value = newEvent;
    visible.value = true;
    // Emit event creation
    // emit("createEvent", newEvent);
  }

  // Reset creation state
  isCreating.value = false;
  createStartY.value = 0;
  createCurrentY.value = 0;
  createStartMinutes.value = 0;
  document.body.style.userSelect = "";
};
</script>
