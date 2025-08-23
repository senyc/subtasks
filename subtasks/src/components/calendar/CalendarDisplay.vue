<template>
  <section class="h-full w-full flex flex-col pl-7">
    <CalendarHeader :scope="scope" :span="span" />
    <Calendar :scope="scope" :span="span" />
  </section>
</template>

<script setup lang="ts">
import type { CalendarSpan } from "@annotations/calendarSpan";
import CalendarHeader from "./CalendarHeader.vue";
import Calendar from "./Calendar.vue";
import TimeSideBar from "./TimeSideBar.vue";

defineProps<{
  span: CalendarSpan;
  scope: Date;
}>();
</script>
