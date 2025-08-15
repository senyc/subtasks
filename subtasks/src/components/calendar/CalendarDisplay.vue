<template>
  <section class="h-full w-full flex flex-col pl-7 pb-7">
    <CalendarHeader :scope="scope" :span="span" />
    <div class="flex h-full w-full flex-row">
      <TimeSideBar v-if="span !== 'month'" />
      <div class="flex flex-col w-full">
        <Calendar :scope="scope" :span="span" />
      </div>
    </div>
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
