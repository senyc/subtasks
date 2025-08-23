<template>
  <div class="pl-1 flex flex-col gap-2">
    <h2 class="text-center font-bold text-xl">
      {{ date.toLocaleString("en-US", { weekday: "short" }) }}
    </h2>
    <h3
      class="w-8 h-8 font-bold text-xl"
      :class="{
        'bg-blue-500 inline-flex flex-row items-center justify-center px-2 rounded-full text-white':
          date.toDateString() == new Date().toDateString(),
      }"
    >
      {{ date.getDate() }}
    </h3>
  </div>
</template>
<script setup lang="ts">
defineProps<{
  date: Date;
}>();
</script>
