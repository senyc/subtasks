<template>
  <div class="h-6 relative" ref="dropdownRef">
    <button class="cursor-pointer" @click="isOpen = !isOpen">
      <slot name="button">Open</slot>
    </button>
    <div
      :class="{ block: isOpen, hidden: !isOpen }"
      class="absolute border border-gray-300 shadow-lg rounded-lg bg-white z-50 w-52 p-3"
      v-if="isOpen"
    >
      <slot></slot>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, ref } from "vue";

const isOpen = ref(false);
const dropdownRef = ref<HTMLElement | null>(null);

// closes the dropdown
const handleClickOutside = (event: MouseEvent): void => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target as Node)) {
    isOpen.value = false;
  }
};

// Adds event handler to document that will close the dropdown
onMounted(() => {
  document.addEventListener("click", handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener("click", handleClickOutside);
});
</script>
