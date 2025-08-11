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

    <Event
      v-if="timeSlot.type === 'event'"
      :time-range="timeRange"
      :title="timeSlot.title"
    />

    <Task
      v-if="timeSlot.type === 'task'"
      :time-estimate="eventHeight"
      :title="timeSlot.title"
    />

    <!-- Resize handle -->
    <div class="resize-handle" @mousedown.stop="startResizeBottom"></div>
  </div>
  <Dialog
    :close-on-escape="true"
    draggable
    v-model:visible="visible"
    header="Update Event"
    class="sm:w-100 w-9/10"
  >
    <TimeSlotForm
      @submit="updateEvent"
      v-if="eventModel"
      v-model:model-value="eventModel"
    />
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
import type { Event as EventType } from "@annotations/event";
import type { Task as TaskType } from "@annotations/models/task";
import Event from "./Event.vue";
import Task from "./Task.vue";
import { ref } from "vue";
import { useDeleteEvent, useUpdateEvent } from "@/composables/useEvent";
import { useToast } from "primevue";
const { mutate: mutateEvent } = useUpdateEvent();
const { mutate: mutateTask } = useUpdateTask();
const toast = useToast();
import Dialog from "@volt/Dialog.vue";
import Button from "@volt/Button.vue";
import SecondaryButton from "@volt/SecondaryButton.vue";
import TimeSlotForm from "./events/TimeSlotForm.vue";
import DangerButton from "@volt/DangerButton.vue";
import type {
  TimeSlotForm as TimeSlotFormType,
  TimeSlotResponse,
} from "@/annotations/models/timeSlot";
import { useUpdateTask } from "@/composables/useTasks";

const props = defineProps<{
  /** This can be either a saved timeslot (with an id) or an in-progress timeslot (currently saved within the form)*/
  timeSlot: TimeSlotFormType | TimeSlotResponse;
}>();

const eventModel = ref({ ...props.timeSlot });
const { mutate: deleteEvent } = useDeleteEvent();

function onDelete() {
  if ("id" in props.timeSlot) {
    deleteEvent({ eventId: props.timeSlot?.id });
  } else {
    console.error("Cannot delete without id");
  }
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
  startTime: () => props.timeSlot.start_at,
  endTime: () => props.timeSlot.end_at,
  onResizeEnd: () => {
    if (props.timeSlot.type === "event") {
      mutateEvent({
        event: {
          end_at: actualEndTime.value,
          start_at: actualStartTime.value,
        },
        eventId: (props.timeSlot as TimeSlotResponse).id,
      });
    } else if (props.timeSlot.type === "task") {
      mutateTask({
        task: {
          title: props.timeSlot.title,
          end_at: actualEndTime.value,
          start_at: actualStartTime.value,
        },
        taskId: (props.timeSlot as TimeSlotResponse).id,
      });
    }
  },
});

const visible = ref(false);
function updateEvent() {
  if (!("id" in props.timeSlot)) {
    toast.add({ severity: "error", detail: "Unable to edit event" });
    return;
  }
  if (props.timeSlot.type === "event") {
    const updatedTimeSLot: EventType = {
      title: eventModel.value.title,
      notes: eventModel.value.notes || "",
      is_recurring: false,
    };
    mutateEvent({ event: updatedTimeSLot, eventId: props.timeSlot.id });
    visible.value = false;
  } else if (props.timeSlot.type === "task") {
    const updatedTimeSLot: TaskType = {
      title: eventModel.value.title,
    };
    mutateTask({ task: updatedTimeSLot, taskId: props.timeSlot.id });
    visible.value = false;
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
