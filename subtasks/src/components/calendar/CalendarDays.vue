<template>
  <section
    :class="{
      'grid-cols-7': span === 'week' || span === 'month',
      'grid-cols-1': span === 'day',
    }"
    class="h-full grid gap-4"
  >
    <div
      v-if="span === 'month' && dates[0].getDay() !== 0"
      v-for="_ in dates[0].getDay()"
    ></div>
    <DayPanel v-for="date in dates" :date="date" />
  </section>
</template>

<script setup lang="ts">
import type { CalendarSpan } from "@annotations/calendarSpan";
import DayPanel from "./DayPanel.vue";
import { computed } from "vue";

const { span, scope } = defineProps<{
  span: CalendarSpan;
  scope: Date;
}>();

const getFirstDayOfWeek = (date = new Date()) => {
  const d = new Date(date);
  d.setDate(d.getDate() - d.getDay());
  return d;
};

const startDate = getFirstDayOfWeek(scope);

const daysInMonth = new Date(
  new Date().getFullYear(),
  scope.getMonth(),
  0,
).getDate();

const dates = computed(() =>
  span === "month"
    ? Array.from(
        { length: daysInMonth + 1 },
        (_, i) => new Date(new Date().getFullYear(), scope.getMonth(), i + 1),
      )
    : span === "week"
      ? Array.from({ length: 7 }, (_, i) => {
          const d = new Date(startDate);
          d.setDate(startDate.getDate() + i);
          return d;
        })
      : [scope],
);
</script>
