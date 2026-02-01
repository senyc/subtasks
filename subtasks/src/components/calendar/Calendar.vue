<template>
  <div class="flex flex-col w-full h-full">
    <section
      :class="{
        'divide-y divide-y-black/30': span === 'month',
        'grid-cols-7': span === 'week' || span === 'month',
        'grid-cols-1': span === 'day',
      }"
      class="grow ml-18 w-full divide-x border-x border-x-black/30 divide-black/30 grid"
    ></section>
    <div class="h-full w-full flex-row flex">
      <TimeSideBar v-if="span !== 'month'" />
      <div class="flex w-full h-full flex-col">
        <div
          class="grid grid-cols-7 divide-x border-x border-x-black/30 divide-black/30 grow w-full"
        >
          <!-- Fix this for month view-->
          <PanelHeader
            :key="date.getDate()"
            v-for="date in dates"
            :date="date"
          />
        </div>
        <div
          :class="{
            'divide-y divide-y-black/30': span === 'month',
            'grid-cols-7': span === 'week' || span === 'month',
            'grid-cols-1': span === 'day',
          }"
          class="relative divide-x border-x border-x-black/30 divide-black/30 grow h-full grid w-full mb-1"
        >
          <Panel
            @create-time-slot="createTimeSlot"
            :key="date.getDate()"
            v-for="date in dates"
            :date="date"
          />
          <TimeSlot
            :key="timeSlot.id"
            :full-screen="span === 'day'"
            v-for="timeSlot in timeSlots"
            :time-slot="timeSlot"
            @clone-time-slot="
              (e) => {
                clonedTimeSlot = e;
              }
            "
          />
          <TimeSlot
            v-if="clonedTimeSlot && cloned"
            :key="clonedTimeSlot.end_at"
            :full-screen="span === 'day'"
            :time-slot="clonedTimeSlot"
            @clone-time-slot="
              (e) => {
                clonedTimeSlot = e;
              }
            "
          />
        </div>
      </div>
    </div>
  </div>
  <NewTimeSlot
    @create-time-slot="
      (e: TimeSlotForm) => {
        createTimeSlot(e);
        cloned = false;
        visible = false;
      }
    "
    @cancel-time-slot="cancelTimeSlot"
    v-model:timeSlot="clonedTimeSlot!"
    v-model:visible="visible"
  />
</template>

<script setup lang="ts">
import type { CalendarSpan } from "@/annotations/calendarSpan";
import { computed, onMounted, onUnmounted, ref } from "vue";
import Panel from "./Panel.vue";
import PanelHeader from "./PanelHeader.vue";
import TimeSlot from "./timeslots/TimeSlot.vue";
import TimeSideBar from "./TimeSideBar.vue";
import type { TimeSlotForm } from "@/annotations/models/timeSlot";
import { useCreateEvent } from "@/composables/useEvent";
import { useCreateTask } from "@/composables/useTasks";
import { useCalendar } from "@/composables/useCalendar";
const { mutate: createEvent } = useCreateEvent();
const { mutate: createTask } = useCreateTask();
import NewTimeSlot from "./timeslots/NewTimeSlot.vue";

import CurrentTimeBar from "./CurrentTimeBar.vue";
const props = defineProps<{
  span: CalendarSpan;
  scope: Date;
}>();

const clonedTimeSlot = ref<TimeSlotForm>();
const visible = ref(false);
const cloned = ref(false);

function cancelTimeSlot() {
  clonedTimeSlot.value = undefined;
}

function createTimeSlot(timeSlot: TimeSlotForm) {
  if (timeSlot.type === "event") {
    createEvent({
      event: {
        ...timeSlot,
        end_at: new Date(timeSlot.end_at),
        start_at: new Date(timeSlot.start_at),
      },
    });
  } else if (timeSlot.type === "task") {
    const endAt = new Date(timeSlot.end_at);
    const startAt = new Date(timeSlot.start_at);
    createTask({
      task: {
        ...timeSlot,
        start_at: startAt,
        end_at: endAt,
        body: timeSlot.notes || "",
        //@ts-ignore
        time_estimate: (endAt - startAt) / (1000 * 60),
      },
    });
  } else {
    throw new Error("Invalid type");
  }
}

const dates = computed(() => {
  const daysInMonth = new Date(
    props.scope.getFullYear(),
    props.scope.getMonth() + 1,
    0,
  ).getDate();

  const getFirstDayOfWeek = (date = new Date()) => {
    const d = new Date(date);
    d.setDate(d.getDate() - d.getDay());
    return d;
  };

  const startDate = getFirstDayOfWeek(props.scope);

  return props.span === "month"
    ? Array.from(
        { length: daysInMonth },
        (_, i) =>
          new Date(props.scope.getFullYear(), props.scope.getMonth(), i + 1),
      )
    : props.span === "week"
      ? Array.from({ length: 7 }, (_, i) => {
          const d = new Date(startDate);
          d.setDate(startDate.getDate() + i);
          return d;
        })
      : [props.scope];
});

const { data: timeSlots } = useCalendar({
  startTime: () => dates.value[0],
  endTime: () => {
    const date = dates.value[dates.value.length - 1];

    const midnight = new Date(date);
    midnight.setHours(24);
    return midnight;
  },
});

function updateMousePos(e: MouseEvent) {
  mousePos.value = { x: e.clientX, y: e.clientY };
}

const mousePos = ref({ x: 0, y: 0 });

function cloneEventToPanel({
  timeSlot,
  date,
  time,
}: {
  timeSlot: TimeSlotForm;
  date: string;
  time: { hour: number; minutes: number };
}) {
  const diff =
    Number(new Date(timeSlot.end_at)) - Number(new Date(timeSlot.start_at));

  const baseDate = new Date(date);
  baseDate.setHours(time.hour, time.minutes, 0, 0);

  const newStart = baseDate;
  const newEnd = new Date(newStart.getTime() + diff);

  clonedTimeSlot.value = {
    ...clonedTimeSlot.value!,
    start_at: newStart.toISOString(),
    end_at: newEnd.toISOString(),
    notes: clonedTimeSlot.value!.notes || undefined,
  };

  cloned.value = true;
  visible.value = true;
}

function handleKeydown(e: KeyboardEvent) {
  if (e.ctrlKey && e.key.toLowerCase() === "v") {
    const { x, y } = mousePos.value;
    const panelEl = document.elementFromPoint(x, y)?.closest(".panel") as HTMLElement | null;
    const panelHour = document.elementFromPoint(x, y)?.closest(".hour") as HTMLElement | null;

    if (panelEl && panelHour) {
      cloneEventToPanel({
        timeSlot: clonedTimeSlot.value!,
        date: panelEl.dataset.date!,
        time: { hour: Number(panelHour.dataset.hour), minutes: 0 },
      });
    } else {
      console.error("Cursor not in bounding box");
    }
  }
}

onMounted(() => {
  window.addEventListener("keydown", handleKeydown);
  window.addEventListener("mousemove", updateMousePos);
});

onUnmounted(() => {
  window.removeEventListener("mousemove", updateMousePos);
  window.removeEventListener("keydown", handleKeydown);
});
</script>
