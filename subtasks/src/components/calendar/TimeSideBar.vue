<template>
  <div class="mt-28 grid text-right mr-3 w-18 grid-cols-1 grid-rows-23">
    <p v-for="hour in 23">
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
</template>

<script setup lang="ts">
const date = new Date();
</script>
