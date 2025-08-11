import { computed, onUnmounted, ref } from "vue";
import { toValue, type MaybeRefOrGetter } from "vue";

interface UseEventResizeParams {
  startTime?: MaybeRefOrGetter<string>;
  endTime?: MaybeRefOrGetter<string>;
  onResizeEnd?: () => void;
}

export default function useEventResize({
  startTime,
  endTime,
  onResizeEnd,
}: UseEventResizeParams) {
  // @ts-ignore
  const minDiff = (new Date(toValue(endTime)) - new Date(toValue(startTime))) / (1000 * 60);
  // @ts-ignore
  const midnight = new Date(toValue(startTime));
  midnight.setHours(0, 0, 0, 0);
  // @ts-ignore
  const initialStartMargin = (new Date(toValue(startTime ))- midnight) / (1000 * 60);

  const eventHeight = ref(minDiff);
  const startMargin = ref(initialStartMargin);
  const isDragging = ref(false);
  const resizeType = ref<"top" | "bottom" | null>(null);
  const startY = ref(0);
  const startHeight = ref(0);
  const startPosition = ref(0);

  const HOUR_HEIGHT = 60;
  const MIN_HEIGHT = 60; // 1 hour minimum
  const MAX_HEIGHT = 1440; // 24 hours maximum
  const SNAP_INTERVAL = 15; // 15 minute intervals

  // Start resizing from top handle - using mousedown with dragover simulation
  const startResizeTop = (e: MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();

    isDragging.value = true;
    resizeType.value = "top";
    startY.value = e.clientY;
    startHeight.value = eventHeight.value;
    startPosition.value = startMargin.value;

    // Use mousemove instead of drag events for reliable coordinate tracking
    document.addEventListener("mousemove", doResize);
    document.addEventListener("mouseup", stopResize);
    document.body.style.userSelect = "none";
    document.body.style.cursor = "ns-resize";
  };

  // Start resizing from bottom handle
  const startResizeBottom = (e: MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();

    isDragging.value = true;
    resizeType.value = "bottom";
    startY.value = e.clientY;
    startHeight.value = eventHeight.value;
    startPosition.value = startMargin.value;

    document.addEventListener("mousemove", doResize);
    document.addEventListener("mouseup", stopResize);
    document.body.style.userSelect = "none";
    document.body.style.cursor = "ns-resize";
  };

  const doResize = (e: MouseEvent) => {
    if (!isDragging.value || !resizeType.value) return;

    const deltaY = e.clientY - startY.value;
    // Convert pixel movement to minutes (assuming HOUR_HEIGHT = 60px = 60min)
    const deltaMinutes = deltaY;

    if (resizeType.value === "bottom") {
      // Resize from bottom - only change height
      let newHeight = startHeight.value + deltaMinutes;
      newHeight = Math.max(MIN_HEIGHT, Math.min(MAX_HEIGHT, newHeight));

      // Snap to intervals
      newHeight = Math.round(newHeight / SNAP_INTERVAL) * SNAP_INTERVAL;
      eventHeight.value = newHeight;
    } else if (resizeType.value === "top") {
      // Resize from top - change both position and height
      let newStartMargin = startPosition.value + deltaMinutes;
      let newHeight = startHeight.value - deltaMinutes;

      // Ensure minimum height
      if (newHeight < MIN_HEIGHT) {
        const adjustment = MIN_HEIGHT - newHeight;
        newHeight = MIN_HEIGHT;
        newStartMargin = startPosition.value + deltaMinutes - adjustment;
      }

      // Don't allow dragging before midnight or after 24 hours
      newStartMargin = Math.max(0, Math.min(1440 - newHeight, newStartMargin));

      // Snap to intervals
      newStartMargin =
        Math.round(newStartMargin / SNAP_INTERVAL) * SNAP_INTERVAL;
      newHeight = Math.round(newHeight / SNAP_INTERVAL) * SNAP_INTERVAL;

      startMargin.value = newStartMargin;
      eventHeight.value = newHeight;
    }
  };

  const stopResize = () => {
    resizeType.value = null;
    document.removeEventListener("mousemove", doResize);
    document.removeEventListener("mouseup", stopResize);
    document.body.style.userSelect = "";
    document.body.style.cursor = "";
    onResizeEnd();
    setTimeout(() => (isDragging.value = false), 0); // reset after click
  };

  // Computed properties
  const hourCount = computed(() => eventHeight.value / 60);

  const actualStartTime = computed(() => {
    const newStart = new Date(midnight);
    newStart.setMinutes(startMargin.value);
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
      const minutes = date.getMinutes();
      const period = hours >= 12 ? "PM" : "AM";
      const displayHour = hours > 12 ? hours - 12 : hours === 0 ? 12 : hours;
      const displayMinutes = minutes.toString().padStart(2, "0");
      return `${displayHour}:${displayMinutes} ${period}`;
    };

    return `${formatTime(actualStartTime.value)} - ${formatTime(actualEndTime.value)}`;
  });

  // Cleanup on unmount
  onUnmounted(() => {
    document.removeEventListener("mousemove", doResize);
    document.removeEventListener("mouseup", stopResize);
  });

  return {
    eventHeight,
    startMargin,
    isDragging,
    resizeType,
    hourCount,
    timeRange,
    actualStartTime,
    actualEndTime,
    HOUR_HEIGHT,
    // Recommended mouse-based approach
    startResizeTop,
    startResizeBottom,
  };
}
