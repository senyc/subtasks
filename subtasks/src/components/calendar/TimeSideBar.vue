<template>
  <div
    class="grid text-right min-w-17 h-[calc(100%-75px)] mt-auto mb-3 mr-3 grow grid-cols-1 grid-rows-24"
  >
    <p
      class="text-sm"
      v-for="hour in 24"
      :key="hour"
    >
      {{
        new Date(
          date.getFullYear(),
          date.getMonth(),
          date.getDate(),
          hour - 1, // because v-for starts at 1
          0,
          0
        ).toLocaleTimeString("en-US", {
          hour: "numeric",
        })
      }}
    </p>
  </div>
</template>

<script setup lang="ts">
const date = new Date();
</script>
