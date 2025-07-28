<template>
  <div
    class="event-box select-none"
    @click.stop="() => !isDragging && (visible = true)"
    :style="{
      top: `calc((${startMargin} / (24 * 60)) * 100% - 29px)`,
      height: `${(eventHeight / (24 * 60)) * 100}%`,
    }"
  >
    <div class="resize-handle-top" @mousedown.stop="startResizeTop"></div>
    <div class="event-content">
      <div class="event-title">{{ event.title || "New Event" }}</div>
      <div class="event-time">{{ timeRange }}</div>
    </div>

    <!-- Resize handle -->
    <div class="resize-handle" @mousedown.stop="startResizeBottom"></div>
  </div>
  <Dialog
    :close-on-escape="true"
    :draggable="false"
    v-model:visible="visible"
    modal
    header="Update Event"
    class="sm:w-100 w-9/10"
  >
    <EventForm v-if="eventModel" :event="eventModel" />
    <div class="flex justify-between gap-2">
      <div class="flex flex-row gap-2">
        <DangerButton severity="danger" type="button" @click="onDelete"
          >Delete</DangerButton
        >
        <SecondaryButton
          type="button"
          label="Cancel"
          @click="visible = false"
        />
      </div>
      <Button type="button" label="Save" @click="updateEvent" />
    </div>
  </Dialog>
</template>

<script setup lang="ts">
import useEventResize from "@composables/useEventResize";
import type { Event } from "@annotations/event";
import { computed, ref } from "vue";
import { useDeleteEvent, useUpdateEvent } from "@composables/useEvents";
import { useToast } from "primevue";
const { mutate } = useUpdateEvent();
const toast = useToast();
import Dialog from "@volt/Dialog.vue";
import Button from "@volt/Button.vue";
import SecondaryButton from "@volt/SecondaryButton.vue";
import EventForm from "./EventForm.vue";
import DangerButton from "@volt/DangerButton.vue";
const props = defineProps<{
  event: Event & { id?: number };
}>();
const eventModel = ref({ ...props.event });
const { mutate: deleteEvent } = useDeleteEvent();

function onDelete() {
  deleteEvent({ eventId: props.event.id! });
}
const {
  eventHeight,
  startMargin,
  actualStartTime,
  actualEndTime,
  timeRange,
  startResizeTop,
  isDragging,
  startResizeBottom,
} = useEventResize({
  startTime: new Date(props.event.start_at),
  endTime: new Date(props.event.end_at),
  onResizeEnd: () =>
    mutate({
      event: { end_at: actualEndTime.value, start_at: actualStartTime.value },
      eventId: props.event.id!,
    }),
});

const visible = ref(false);
function updateEvent() {
  if (props.event.id) {
    const updatedEvent: Event = {
      title: eventModel.value.title,
      notes: eventModel.value.notes || "",
      is_recurring: false,
    };
    mutate({ event: updatedEvent, eventId: props.event.id });
    visible.value = false;
  } else {
    toast.add({ severity: "error", detail: "Unable to edit event" });
  }
}
const mouseDownTime = ref(0);
</script>

<style>
.event-box {
  position: absolute;
  left: 8px;
  right: 8px;
  top: 0;
  background: #4285f4;
  color: white;
  border-radius: 4px;
  min-height: 60px;
  cursor: default;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.event-content {
  padding: 8px 12px;
  pointer-events: none;
}

.event-title {
  font-weight: 600;
  font-size: 14px;
  margin-bottom: 4px;
}

.event-time {
  font-size: 12px;
  opacity: 0.9;
}

.resize-handle {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 8px;
  background: rgba(255, 255, 255, 0.2);
  cursor: ns-resize;
  border-radius: 0 0 4px 4px;
}

.resize-handle:hover {
  background: rgba(255, 255, 255, 0.3);
}

.resize-handle::after {
  content: "";
  position: absolute;
  bottom: 2px;
  left: 50%;
  transform: translateX(-50%);
  width: 20px;
  height: 2px;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 1px;
}

.resize-handle-top {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 8px;
  background: rgba(255, 255, 255, 0.2);
  cursor: ns-resize;
  border-radius: 0 0 4px 4px;
}

.resize-handle-top:hover {
  background: rgba(255, 255, 255, 0.3);
}

.resize-handle-top::after {
  content: "";
  position: absolute;
  bottom: 2px;
  left: 50%;
  transform: translateX(-50%);
  width: 20px;
  height: 2px;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 1px;
}

.dragging {
  user-select: none;
}

.info {
  text-align: center;
  margin-bottom: 20px;
  color: #666;
}
</style>
