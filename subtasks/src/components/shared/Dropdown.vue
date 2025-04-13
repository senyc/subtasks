<template>
  <div class="h-6 relative" ref="dropdownRef">
    <button class="cursor-pointer" @click="isOpen = !isOpen">
      <slot name="button">Open</slot>
    </button>
    <div
      :class="{ block: isOpen, hidden: !isOpen }"
      class="absolute border border-gray-300 shadow-lg rounded-lg bg-white z-50 w-96 p-3"
      v-if="isOpen"
    >
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, ref } from "vue";

const isOpen = ref(false);
const dropdownRef = ref<HTMLElement | null>(null);

const isClickOnModalBackdrop = (event: MouseEvent): boolean => {
  const target = event.target as HTMLElement;

  // Check if the user is clicking on a modal or button
  return target.classList.contains("h-modal") || !!target.closest("button");
};

const handleClickOutside = (event: MouseEvent): void => {
  if (isClickOnModalBackdrop(event)) {
    return;
  }

  if (dropdownRef.value && !dropdownRef.value.contains(event.target as Node)) {
    isOpen.value = false;
  }
};

onMounted(() => {
  document.addEventListener("click", handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener("click", handleClickOutside);
});
</script>
