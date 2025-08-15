import { computed, onUnmounted, ref, watch } from "vue";
import { toValue, type MaybeRefOrGetter } from "vue";

interface UseEventResizeParams {
  startTime: MaybeRefOrGetter<string>;
  endTime: MaybeRefOrGetter<string>;
  onResizeEnd?: () => void;
}

export default function useEventResize({
  startTime,
  endTime,
  onResizeEnd,
}: UseEventResizeParams) {
  const minDiff =
    (new Date(toValue(endTime)).getTime() -
      new Date(toValue(startTime)).getTime()) /
    (1000 * 60);
  const midnight = new Date(toValue(startTime));
  midnight.setHours(0, 0, 0, 0);
  const initialStartMargin =
    (new Date(toValue(startTime)).getTime() - midnight.getTime()) / (1000 * 60);

  const eventHeight = ref(minDiff);
  const startMargin = ref(initialStartMargin); // minutes from midnight
  const left = ref(0); // horizontal offset (e.g., day column position)

  const isDragging = ref(false);
  const resizeType = ref<"top" | "bottom" | null>(null);

  const startY = ref(0);
  const startX = ref(0);
  const startHeight = ref(0);
  const startPosition = ref(0); // minutes from midnight at drag start
  const startLeft = ref(0); // left offset at drag start

  const HOUR_HEIGHT = 60;
  const MIN_HEIGHT = 60; // 1 hour
  const MAX_HEIGHT = 1440; // 24 hours
  const SNAP_INTERVAL = 15; // minutes
  const snapX = window.innerWidth / 7; // width per day column

  /** ---------------- RESIZE (TOP) ---------------- **/
  const startResizeTop = (e: MouseEvent) => {
    e.preventDefault();
    isDragging.value = true;
    resizeType.value = "top";
    startY.value = e.clientY;
    startHeight.value = eventHeight.value;
    startPosition.value = startMargin.value;

    document.addEventListener("mousemove", doResize);
    document.addEventListener("mouseup", stopResize);
    document.body.style.userSelect = "none";
    document.body.style.cursor = "ns-resize";
  };
  /** ---------------- RESIZE (BOTTOM) ---------------- **/
  const startResizeBottom = (e: MouseEvent) => {
    e.preventDefault();
    isDragging.value = true;
    resizeType.value = "bottom";
    startY.value = e.clientY;
    startHeight.value = eventHeight.value;

    document.addEventListener("mousemove", doResize);
    document.addEventListener("mouseup", stopResize);
    document.body.style.userSelect = "none";
    document.body.style.cursor = "ns-resize";
  };

  const dragged = ref(false);
  /** ---------------- MOVE (DRAG) ---------------- **/
  const startDrag = (e: MouseEvent) => {
    e.preventDefault();
    dragged.value = false;
    isDragging.value = true;
    resizeType.value = null; // not resizing, just moving
    startX.value = e.clientX;
    startY.value = e.clientY;
    startPosition.value = startMargin.value;
    startLeft.value = left.value;

    document.addEventListener("mousemove", onDrag);
    document.addEventListener("mouseup", stopDrag);
    document.body.style.userSelect = "none";
    document.body.style.cursor = "move";
  };

  const onDrag = (e: MouseEvent) => {
    if (!isDragging.value || resizeType.value) return;

    const deltaY = e.clientY - startY.value;
    const deltaX = e.clientX - startX.value;

    // Vertical movement in minutes
    let newStartMargin = startPosition.value + deltaY;
    newStartMargin = Math.max(
      0,
      Math.min(1440 - eventHeight.value, newStartMargin),
    );
    newStartMargin = Math.round(newStartMargin / SNAP_INTERVAL) * SNAP_INTERVAL;

    // Horizontal movement in days
    let newLeft = startLeft.value + deltaX;
    newLeft = Math.round(newLeft / snapX) * snapX; // snap to day column

    startMargin.value = newStartMargin;
    left.value = newLeft;
  };

  const stopDrag = () => {
    isDragging.value = false;
    document.removeEventListener("mousemove", onDrag);
    document.removeEventListener("mouseup", stopDrag);
    document.body.style.userSelect = "";
    document.body.style.cursor = "";
    if (dragged.value) onResizeEnd?.();
  };

  /** ---------------- RESIZE HANDLER ---------------- **/
  const doResize = (e: MouseEvent) => {
    if (!isDragging.value || !resizeType.value) return;

    const deltaY = e.clientY - startY.value;
    const deltaMinutes = deltaY;

    if (resizeType.value === "bottom") {
      let newHeight = startHeight.value + deltaMinutes;
      newHeight = Math.max(MIN_HEIGHT, Math.min(MAX_HEIGHT, newHeight));
      eventHeight.value = Math.round(newHeight / SNAP_INTERVAL) * SNAP_INTERVAL;
    } else if (resizeType.value === "top") {
      let newStartMargin = startPosition.value + deltaMinutes;
      let newHeight = startHeight.value - deltaMinutes;

      if (newHeight < MIN_HEIGHT) {
        const adjustment = MIN_HEIGHT - newHeight;
        newHeight = MIN_HEIGHT;
        newStartMargin -= adjustment;
      }

      newStartMargin = Math.max(0, Math.min(1440 - newHeight, newStartMargin));
      startMargin.value =
        Math.round(newStartMargin / SNAP_INTERVAL) * SNAP_INTERVAL;
      eventHeight.value = Math.round(newHeight / SNAP_INTERVAL) * SNAP_INTERVAL;
    }
  };

  const stopResize = () => {
    isDragging.value = false;
    resizeType.value = null;
    document.removeEventListener("mousemove", doResize);
    document.removeEventListener("mouseup", stopResize);
    document.body.style.userSelect = "";
    document.body.style.cursor = "";
    onResizeEnd?.();
  };

  /** ---------------- COMPUTED ---------------- **/
  const hourCount = computed(() => eventHeight.value / 60);

  const currentDayIndex = computed(() => {
    // Number of columns moved from original day
    return Math.round(left.value / snapX);
  });
  const currentDay = computed(() => actualStartTime.value.getDay());

  const actualStartTime = computed(() => {
    const newStart = new Date(midnight);
    newStart.setMinutes(startMargin.value);
    // Adjust by how many days horizontally dragged
    newStart.setDate(newStart.getDate() + currentDayIndex.value);
    return newStart;
  });

  const actualEndTime = computed(() => {
    const newEnd = new Date(actualStartTime.value);
    newEnd.setMinutes(newEnd.getMinutes() + eventHeight.value);
    return newEnd;
  });

  const timeRange = computed(() => {
    const formatTime = (date: Date) => {
      const hours = date.getHours();
      const minutes = date.getMinutes().toString().padStart(2, "0");
      const period = hours >= 12 ? "PM" : "AM";
      const displayHour = hours % 12 || 12;
      return `${displayHour}:${minutes} ${period}`;
    };
    return `${formatTime(actualStartTime.value)} - ${formatTime(actualEndTime.value)}`;
  });

  watch(actualStartTime, (newVal, oldVal) => {
    if (newVal !== oldVal) {
      dragged.value = true;
    }
  });

  // Watch for time range changes
  watch(timeRange, (newVal, oldVal) => {
    if (newVal !== oldVal) {
      dragged.value = true;
    }
  });
  /** ---------------- CLEANUP ---------------- **/
  onUnmounted(() => {
    document.removeEventListener("mousemove", doResize);
    document.removeEventListener("mouseup", stopResize);
    document.removeEventListener("mousemove", onDrag);
    document.removeEventListener("mouseup", stopDrag);
  });

  return {
    eventHeight,
    startMargin,
    left,
    isDragging,
    resizeType,
    hourCount,
    currentDayIndex,
    timeRange,
    dragged,
    actualStartTime,
    actualEndTime,
    HOUR_HEIGHT,
    startResizeTop,
    currentDay,
    startResizeBottom,
    startDrag,
  };
}
