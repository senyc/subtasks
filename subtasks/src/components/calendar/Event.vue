<template>
  <div
    ref="eventBox"
    class="event-box"
    :style="{
      top: `calc((${startMargin} / (24 * 60)) * 100% - 29px)`,
      height: `${(eventHeight / (24 * 60)) * 100}%`,
    }"
  >
    <div class="resize-handle-top" @mousedown="startResizeTop"></div>
    <div class="event-content">
      <div class="event-title">Team Meeting</div>
      <div class="event-time">{{ timeRange }}</div>
    </div>

    <!-- Resize handle -->
    <div class="resize-handle" @mousedown="startResizeBottom"></div>
  </div>
</template>

<script setup lang="ts">
import useEventResize from "@composables/useEventResize";
import type EventType from "@annotations/event";

const props = defineProps<{
  event: EventType;
}>();

const {
  eventHeight,
  startMargin,
  timeRange,
  startResizeTop,
  startResizeBottom,
} = useEventResize({
  startTime: props.event.start_at,
  endTime: props.event.end_at,
});
</script>

<style>
.event-box {
  position: absolute;
  left: 8px;
  right: 8px;
  top: 0;
  background: #4285f4;
  color: white;
  border-radius: 4px;
  min-height: 60px;
  cursor: default;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.event-content {
  padding: 8px 12px;
  pointer-events: none;
}

.event-title {
  font-weight: 600;
  font-size: 14px;
  margin-bottom: 4px;
}

.event-time {
  font-size: 12px;
  opacity: 0.9;
}

.resize-handle {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 8px;
  background: rgba(255, 255, 255, 0.2);
  cursor: ns-resize;
  border-radius: 0 0 4px 4px;
}

.resize-handle:hover {
  background: rgba(255, 255, 255, 0.3);
}

.resize-handle::after {
  content: "";
  position: absolute;
  bottom: 2px;
  left: 50%;
  transform: translateX(-50%);
  width: 20px;
  height: 2px;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 1px;
}

.resize-handle-top {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 8px;
  background: rgba(255, 255, 255, 0.2);
  cursor: ns-resize;
  border-radius: 0 0 4px 4px;
}

.resize-handle-top:hover {
  background: rgba(255, 255, 255, 0.3);
}

.resize-handle-top::after {
  content: "";
  position: absolute;
  bottom: 2px;
  left: 50%;
  transform: translateX(-50%);
  width: 20px;
  height: 2px;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 1px;
}

.dragging {
  user-select: none;
}

.info {
  text-align: center;
  margin-bottom: 20px;
  color: #666;
}
</style>
