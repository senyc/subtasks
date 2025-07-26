<template>
  <section
    class="flex flex-row pb-3 pt-3 justify-between items-center gap-5 mr-0.5"
  >
    <h1 class="text-3xl font-bold">{{ calendarHeader }}</h1>
    <select
      class="rounded-md border p-2"
      @change="
        (e: Event) => {
          const span = (e.target as HTMLSelectElement).value;
          $router.push(`/calendar/${span}`);
        }
      "
      :value="type"
    >
      <option v-for="span in spans" :key="span" :value="span">
        {{ span.slice(0, 1).toUpperCase() + span.slice(1) }}
      </option>
    </select>
  </section>
</template>

<script setup lang="ts">
import { computed } from "vue";

const props = defineProps<{
  type: "month" | "week" | "day";
  scope: Date;
}>();

// Can't desctructure props because of how the precompiler works with defineModel

const spans = ["month", "week", "day"];

const calendarHeader = computed(() => {
  const defaultHeader = `${props.scope.toLocaleString("default", { month: "long" })} ${props.scope.getUTCFullYear()}`;
  if (props.type != "week") {
    return defaultHeader;
  }

  const dateToStart = new Date(
    new Date(props.scope).setUTCDate(
      props.scope.getUTCDate() - props.scope.getUTCDay(),
    ),
  );

  const dateToEnd = new Date(
    new Date(dateToStart).setUTCDate(dateToStart.getUTCDate() + 7),
  );

  if (dateToEnd.getUTCMonth() != dateToStart.getUTCMonth()) {
    if (dateToEnd.getUTCFullYear() == dateToStart.getUTCFullYear()) {
      return `${dateToStart.toLocaleString("default", { month: "short" })} - ${dateToEnd.toLocaleString("default", { month: "short" })} ${dateToEnd.getUTCFullYear()}`;
    } else if (dateToEnd.getUTCFullYear() != dateToStart.getUTCFullYear()) {
      return `${dateToStart.toLocaleString("default", { month: "short" })} ${dateToStart.getUTCFullYear()} - ${dateToEnd.toLocaleString("default", { month: "short" })} ${dateToEnd.getUTCFullYear()}`;
    }
  }
  return defaultHeader;
});
</script>
