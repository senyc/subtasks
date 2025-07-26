<template>
  <section class="grid auto-cols-fr grid-flow-col gap-4">
    <div
      class="text-center font-bold"
      v-if="days > 1"
      v-for="day in daysInWeek"
    >
      {{ day }}
    </div>
    <div v-else>{{ daysInWeek[scope.getDay() + 1] }}</div>
  </section>
</template>

<script setup lang="ts">
import type { CalendarSpan } from "@annotations/calendarSpan";

const props = defineProps<{
  span: CalendarSpan;
  scope: Date;
}>();
const days = props.span === "day" ? 1 : 7;

const daysInWeek = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
</script>
