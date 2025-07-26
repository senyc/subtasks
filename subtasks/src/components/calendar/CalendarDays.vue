<template>
  <section
    :class="{
      'grid-cols-7': span === 'week' || span === 'month',
      'grid-cols-1': span === 'day',
      'border-y-black/20 border-y': span !== 'month',
      'border-t-black/20 border-t': span === 'month',
    }"
    class="h-full grid"
  >
    <div
      v-if="span === 'month' && dates[0].getDay() !== 0"
      v-for="_ in dates[0].getDay()"
    ></div>
    <DayPanel
      :card-view="span === 'month'"
      v-for="date in dates"
      :date="date"
    />
  </section>
</template>

<script setup lang="ts">
import type { CalendarSpan } from "@annotations/calendarSpan";
import DayPanel from "./DayPanel.vue";
import { computed } from "vue";

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
</script>
