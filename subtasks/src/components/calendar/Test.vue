<template>
  <div
    class="event"
    :style="{ top: top + 'px', left: left + 'px' }"
    @mousedown="startDrag"
  >
    Drag or Click Me
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

// Position
const top = ref(0);
const left = ref(0);

// Grid sizes
const snapY = 50; // px per time slot
const snapX = 120; // px per day column

// Drag state
let startX = 0;
let startY = 0;
let startTop = 0;
let startLeft = 0;
let hasDragged = false;

function startDrag(e) {
  startX = e.clientX;
  startY = e.clientY;
  startTop = top.value;
  startLeft = left.value;
  hasDragged = false;

  document.addEventListener("mousemove", onDrag);
  document.addEventListener("mouseup", stopDrag);
}

function onDrag(e) {
  const deltaX = e.clientX - startX;
  const deltaY = e.clientY - startY;

  if (Math.abs(deltaX) > 3 || Math.abs(deltaY) > 3) {
    hasDragged = true;
  }

  if (hasDragged) {
    const snappedY = Math.round((startTop + deltaY) / snapY) * snapY;
    const snappedX = Math.round((startLeft + deltaX) / snapX) * snapX;

    top.value = snappedY;
    left.value = snappedX;
  }
}

function stopDrag() {
  document.removeEventListener("mousemove", onDrag);
  document.removeEventListener("mouseup", stopDrag);

  if (!hasDragged) {
    openEditPopup();
  }
}

function openEditPopup() {
  alert("Open edit modal here!");
}
</script>

<style>
.event {
  position: absolute;
  width: 120px; /* same as snapX */
  height: 50px; /* same as snapY */
  background: lightblue;
  border: 1px solid blue;
  cursor: grab;
  user-select: none;
}
</style>
