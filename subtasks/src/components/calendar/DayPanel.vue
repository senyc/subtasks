<template>
  <div
    class="h-full py-2 bg-white"
    :class="{
      'border-b border-l border-l-black/20 border-b-black/20': cardView,
      'border-l-black/20 border-l': !cardView,
    }"
  >
    <h3
      class="font-bold inline-block p-1 text-xl"
      :class="{
        'bg-blue-500 rounded-full text-white':
          date?.toDateString() == new Date().toDateString(),
        'text-center': cardView,
      }"
    >
      {{ date?.getDate() }}
    </h3>
    <div class="grid grid-cols-1 grid-rows-23 h-full mt-1">
      <div class="border-t border-t-black/20 h-3" v-for="_ in 23"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    date: Date;
    cardView?: boolean;
  }>(),
  {
    cardView: false,
  },
);
</script>
