<template>
  <section
    :class="{
      'divide-y divide-y-black/30': span === 'month',
      'grid-cols-7': span === 'week' || span === 'month',
      'grid-cols-1': span === 'day',
    }"
    class="h-full divide-x border-x border-x-black/30 divide-black/30 grid"
  >
    <div
      v-if="span === 'month' && dates[0].getDay() !== 0"
      v-for="_ in dates[0].getDay()"
    ></div>
    <DayPanel
      :card-view="span === 'month'"
      v-for="date in dates"
      :date="date"
      @create-time-slot="
        (timeSlot) => {
          if (timeSlot.type === 'event') {
            createEvent({
              event: {
                ...timeSlot,
                end_at: new Date(timeSlot.end_at),
                start_at: new Date(timeSlot.start_at),
              },
            });
          } else if (timeSlot.type === 'task') {
            const endAt = new Date(timeSlot.end_at);
            const startAt = new Date(timeSlot.start_at);
            createTask({
              task: {
                ...timeSlot,
                start_at: startAt,
                end_at: endAt,
                body: timeSlot.notes || '',
                //@ts-ignore
                time_estimate: (endAt - startAt) / (1000 * 60),
              },
            });
          } else {
            throw new Error('Invalid type');
          }
        }
      "
      :events="
        events?.filter((event) => {
          const dateMidnight = new Date(date);
          dateMidnight.setHours(23);
          return (
            date <= new Date(event.start_at) &&
            dateMidnight > new Date(event.end_at)
          );
        })
      "
    />
  </section>
</template>

<script setup lang="ts">
import type { CalendarSpan } from "@annotations/calendarSpan";
import DayPanel from "./DayPanel.vue";
import { computed } from "vue";
import { useCalendar } from "@/composables/useCalendar";
import { useCreateEvent } from "@/composables/useEvent";
import { useCreateTask } from "@/composables/useTasks";
const { mutate: createEvent } = useCreateEvent();
const { mutate: createTask } = useCreateTask();

const props = defineProps<{
  span: CalendarSpan;
  scope: Date;
}>();

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

const endTime = computed(() => {
  const date = new Date(dates.value[dates.value.length - 1]);
  date.setHours(23);
  return date;
});

const { data: events } = useCalendar({
  startTime: () => dates.value[0],
  endTime: () => endTime.value,
});
</script>
