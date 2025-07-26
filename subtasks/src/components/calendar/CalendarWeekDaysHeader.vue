<template>
  <section class="text-center grid auto-cols-fr grid-flow-col font-bold">
    <p v-if="days > 1" v-for="day in daysInWeek">
      {{ day }}
    </p>
    <p v-else>{{ daysInWeek[scope.getDay()] }}</p>
  </section>
</template>

<script setup lang="ts">
import type { CalendarSpan } from "@annotations/calendarSpan";
import { computed } from "vue";

const props = defineProps<{
  span: CalendarSpan;
  scope: Date;
}>();

const days = computed(() => (props.span === "day" ? 1 : 7));

const daysInWeek = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
</script>
