<template>
  <div
    class="px-2.5 py-0.5 text-nowrap rounded-md select-none me-2 font-bold"
    :style="{ backgroundColor: color, color: textColor }"
  >
    <slot />
    <slot name="delete" />
  </div>
</template>
<script setup lang="ts">
import { computed } from "vue";

const props = defineProps<{ color: string }>();

const textColor = computed(() => {
  const hex = props.color.replace("#", "");
  const r = parseInt(hex.substring(0, 2), 16);
  const g = parseInt(hex.substring(2, 4), 16);
  const b = parseInt(hex.substring(4, 6), 16);

  // Calculate a darker color (reduce brightness)
  const darken = (value: number) => Math.max(0, value - 95);
  return `rgb(${darken(r)}, ${darken(g)}, ${darken(b)})`;
});
</script>
