<template>
  <div class="h-full flex flex-col min-w-17 pt-3 mr-3">
    <div class="grid text-right flex-grow grid-cols-1 grid-rows-24">
      <div></div>
      <p class="" v-for="hour in 24">
        {{
          new Date(
            date.getFullYear(),
            date.getMonth(),
            date.getDate(),
            hour,
            0,
            0,
          ).toLocaleTimeString("en-US", {
            hour: "numeric",
          })
        }}
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
const date = new Date();
</script>
