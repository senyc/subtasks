<template>
  <section class="h-full flex flex-col px-7 pb-7">
    <CalendarHeader :scope="scope" :span="span" />
    <CalendarWeekDays :scope="scope" :span="span" />
    <CalendarDays :scope="scope" :span="span" />
  </section>
</template>

<script setup lang="ts">
import type { CalendarSpan } from "@annotations/calendarSpan";
import CalendarHeader from "./CalendarHeader.vue";
import CalendarWeekDays from "./CalendarWeekDaysHeader.vue";
import CalendarDays from "./CalendarDays.vue";

defineProps<{
  span: CalendarSpan;
  scope: Date;
}>();
</script>
