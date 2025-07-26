<template>
  <div class="h-full flex flex-col gap-2 p-2 bg-white border rounded-md">
    <h3
      class="font-bold w-fit p-1 text-xl"
      :class="{
        'bg-blue-500 rounded-full text-white':
          date?.toDateString() == new Date().toDateString(),
      }"
    >
      {{ date?.getDate() }}
    </h3>
  </div>
</template>

<script setup lang="ts">
defineProps({
  date: Date,
});
</script>
