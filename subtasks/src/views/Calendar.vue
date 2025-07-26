<template>
  <div class="h-screen flex flex-col">
    <Header active="calendar" />
    <div class="px-8">
      <CalendarBreadCrumbs />
    </div>
    <CalendarDisplay
      :span="currentSpan"
      :scope="scope"
    />
  </div>
</template>

<script setup lang="ts">
import type { CalendarSpan } from "@annotations/calendarSpan";
import Header from "@components/Header.vue";
import CalendarBreadCrumbs from "@components/calendar/CalendarBreadCrumbs.vue";
import CalendarDisplay from "@components/calendar/CalendarDisplay.vue";
import { computed } from "vue";
import { useRoute } from "vue-router";
const route = useRoute();

const currentSpan = computed(() => {
  return (route.params.span as CalendarSpan) || "month";
});

const scope = computed(() => {
  let date = new Date();
  if (route.params.year) {
    const year = parseInt(route.params.year as string);
    const month =
      parseInt(route.params.month as string) || new Date().getMonth() + 1;
    const day =
      parseInt(route.params.day as string) || new Date().getDate() + 1;
    date = new Date(year, month - 1, day);
  }
  return date;
});

</script>
