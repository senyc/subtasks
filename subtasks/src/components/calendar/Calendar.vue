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
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { CalendarSpan } from "@/annotations/calendarSpan";
import { computed } from "vue";
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

const props = defineProps<{
  span: CalendarSpan;
  scope: Date;
}>();

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
</script>
