<template>
  <div
    class="z-50 absolute bg-red-500"
    :class="{ 'w-1/7': !fullScreen ,
      'w-full': fullScreen
    }"
    :style="{
      top: 'calc((' + startMargin + ' / (24 * 60)) * 100%)',
      height: '3px',
      left: fullScreen ? '' : 'calc(' + (new Date().getDay() / 7) * 100 + '%)',
    }"
  >
    <div class="absolute -top-1 bg-red-500 rounded-full h-3 w-3 -left-2"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";

defineProps<{
  fullScreen: boolean;
}>();

const startMargin = ref(0);

function updateStartMargin() {
  const midnight = new Date();
  midnight.setHours(0, 0, 0, 0);
  startMargin.value = (Date.now() - midnight.getTime()) / (1000 * 60);
}

onMounted(() => {
  updateStartMargin();
  const interval = setInterval(updateStartMargin, 2000); // every 2 seconds
  onUnmounted(() => clearInterval(interval));
});
</script>
