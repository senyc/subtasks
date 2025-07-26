<template>
  <div class="h-screen flex flex-col">
    <Header active="calendar" />
    <div class="px-8">
      <CalendarBreadCrumbs />
    </div>
    <CalendarDisplay
      :span="($route.params.span as CalendarSpan) || 'month'"
      :scope="new Date()"
    />
  </div>
</template>

<script setup lang="ts">
import type { CalendarSpan } from "@annotations/calendarSpan";
import Header from "@components/Header.vue";
import CalendarBreadCrumbs from "@components/calendar/CalendarBreadCrumbs.vue";
import CalendarDisplay from "@components/calendar/CalendarDisplay.vue";
</script>
