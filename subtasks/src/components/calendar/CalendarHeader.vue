<template>
  <section
    class="flex pr-7 flex-row pb-3 pt-3 justify-between items-center gap-5 mr-0.5"
  >
    <h1 class="text-3xl font-bold">{{ calendarHeader }}</h1>
    <div class="flex flex-row items-center gap-5">
      <div class="flex flex-row items-center">
        <RouterLink :to="backLink">
          <svg
            :class="{}"
            class="size-9 dark:text-white"
            aria-hidden="true"
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            fill="none"
            viewBox="0 0 24 24"
          >
            <path
              stroke="currentColor"
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="m14 8-4 4 4 4"
            />
          </svg>
        </RouterLink>

        <RouterLink :to="forwardLink" class="cursor-pointer">
          <svg
            class="size-9 dark:text-white"
            aria-hidden="true"
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            fill="none"
            viewBox="0 0 24 24"
          >
            <path
              stroke="currentColor"
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="m10 16 4-4-4-4"
            />
          </svg>
        </RouterLink>
      </div>
      <RouterLink
        :to="`/calendar/${span}/${new Date().toLocaleDateString('en-CA').replace(/-/g, '/')}`"
        class="px-3 py-1 font-bold border rounded-lg"
        >Today</RouterLink
      >
      <select
        class="rounded-lg border font-bold p-2"
        @change="
          (e: Event) => {
            const span = (e.target as HTMLSelectElement).value;
            if ($route.params.year) {
              $router.push(
                `/calendar/${span}/${scope.toLocaleDateString('en-CA').replace(/-/g, '/')}`,
              );
            } else {
              $router.push(`/calendar/${span}/`);
            }
          }
        "
        :value="span"
      >
        <option v-for="span in spans" :key="span" :value="span">
          {{ span.slice(0, 1).toUpperCase() + span.slice(1) }}
        </option>
      </select>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from "vue";

const props = defineProps<{
  span: "month" | "week" | "day";
  scope: Date;
}>();

// Can't de-structure props because of how the precompiler works with defineModel

const spans = ["month", "week", "day"];

const calendarHeader = computed(() => {
  const defaultHeader = `${props.scope.toLocaleString("default", { month: "long" })} ${props.scope.getFullYear()}`;
  if (props.span != "week") {
    return defaultHeader;
  }

  const dateToStart = new Date(
    new Date(props.scope).setDate(props.scope.getDate() - props.scope.getDay()),
  );

  const dateToEnd = new Date(
    new Date(dateToStart).setDate(dateToStart.getDate() + 6),
  );

  if (dateToEnd.getMonth() != dateToStart.getMonth()) {
    if (dateToEnd.getFullYear() == dateToStart.getFullYear()) {
      return `${dateToStart.toLocaleString("default", { month: "short" })} - ${dateToEnd.toLocaleString("default", { month: "short" })} ${dateToEnd.getFullYear()}`;
    } else if (dateToEnd.getFullYear() != dateToStart.getUTCFullYear()) {
      return `${dateToStart.toLocaleString("default", { month: "short" })} ${dateToStart.getFullYear()} - ${dateToEnd.toLocaleString("default", { month: "short" })} ${dateToEnd.getFullYear()}`;
    }
  }
  return defaultHeader;
});

const forwardLink = computed(() => {
  const date = new Date(props.scope);
  switch (props.span) {
    case "month":
      date.setMonth(date.getMonth() + 1);
      return `/calendar/month/${date.toLocaleDateString("en-CA").replace(/-/g, "/")}`;
    case "week":
      date.setDate(date.getDate() + 7);
      return `/calendar/week/${date.toLocaleDateString("en-CA").replace(/-/g, "/")}`;
    case "day":
      date.setDate(date.getDate() + 1);
      return `/calendar/day/${date.toLocaleDateString("en-CA").replace(/-/g, "/")}`;
  }
});

const backLink = computed(() => {
  const date = new Date(props.scope);
  switch (props.span) {
    case "month":
      date.setMonth(date.getMonth() - 1);
      return `/calendar/month/${date.toLocaleDateString("en-CA").replace(/-/g, "/")}`;
    case "week":
      date.setDate(date.getDate() - 7);
      return `/calendar/week/${date.toLocaleDateString("en-CA").replace(/-/g, "/")}`;
    case "day":
      date.setDate(date.getDate() - 1);
      return `/calendar/day/${date.toLocaleDateString("en-CA").replace(/-/g, "/")}`;
  }
});
</script>
