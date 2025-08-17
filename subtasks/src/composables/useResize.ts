import { computed, onUnmounted, ref, watch } from "vue";
import { toValue, type MaybeRefOrGetter } from "vue";

interface UseResizeParams {
  startTime: MaybeRefOrGetter<string>;
  endTime: MaybeRefOrGetter<string>;
  onResizeEnd?: () => void;
}

const HOUR_HEIGHT = 60;
const MIN_HEIGHT = HOUR_HEIGHT;
const ONE_DAY = 1440;
const SNAP_INTERVAL_MINUTES = 15;
const DAYS_PER_WEEK = 7;

export default function useResize({
  startTime,
  endTime,
  onResizeEnd,
}: UseResizeParams) {
  const minDiff =
    (new Date(toValue(endTime)).getTime() -
      new Date(toValue(startTime)).getTime()) /
    (1000 * 60);
  const midnight = new Date(toValue(startTime));
  midnight.setHours(0, 0, 0, 0);
  const initialStartMargin =
    (new Date(toValue(startTime)).getTime() - midnight.getTime()) / (1000 * 60);

  const timeSlotHeight = ref(minDiff);
  const startMargin = ref(initialStartMargin); // minutes from midnight
  const left = ref(0); // horizontal offset (e.g., day column position)

  const startY = ref(0);
  const startX = ref(0);
  const startHeight = ref(0);
  const startPosition = ref(0); // minutes from midnight at drag start
  const startLeft = ref(0); // left offset at drag start

  const dragged = ref(false); // Tracks whether the time slot actually moved (used for some onclick logic)
  const snapX = window.innerWidth / DAYS_PER_WEEK; // width per day column

  const startDrag = (e: MouseEvent) => {
    // Not dragged if currently dragging
    dragged.value = false;
    e.preventDefault();
    startX.value = e.clientX;
    startY.value = e.clientY;
    startPosition.value = startMargin.value;
    startLeft.value = left.value;

    document.addEventListener("mousemove", onDrag);
    document.addEventListener("mouseup", stopDrag);
    document.body.style.userSelect = "none";
  };

  const onDrag = (e: MouseEvent) => {
    // Only update the cursor if the user has actually started to move the time slot
    if (dragged.value) {
      document.body.style.cursor = "move";
    }

    const deltaY = e.clientY - startY.value;
    const deltaX = e.clientX - startX.value;

    // Vertical movement in minutes
    let newStartMargin = startPosition.value + deltaY;
    newStartMargin = Math.max(
      0,
      Math.min(1440 - timeSlotHeight.value, newStartMargin),
    );

    newStartMargin =
      Math.round(newStartMargin / SNAP_INTERVAL_MINUTES) *
      SNAP_INTERVAL_MINUTES;

    // Horizontal movement in days
    let newLeft = startLeft.value + deltaX;
    newLeft = Math.round(newLeft / snapX) * snapX; // snap to day column

    startMargin.value = newStartMargin;
    left.value = newLeft;
  };

  const stopDrag = () => {
    document.removeEventListener("mousemove", onDrag);
    document.removeEventListener("mouseup", stopDrag);
    document.body.style.userSelect = "";
    document.body.style.cursor = "";
    if (dragged.value) onResizeEnd?.();
  };

  const startResizeTop = (e: MouseEvent) => {
    e.preventDefault();
    startY.value = e.clientY;
    startHeight.value = timeSlotHeight.value;
    startPosition.value = startMargin.value;

    document.addEventListener("mousemove", doResizeTop);
    document.addEventListener("mouseup", stopResizeTop);
    document.body.style.userSelect = "none";
    document.body.style.cursor = "ns-resize";
  };

  const startResizeBottom = (e: MouseEvent) => {
    e.preventDefault();
    startY.value = e.clientY;
    startHeight.value = timeSlotHeight.value;

    document.addEventListener("mousemove", doResizeBottom);
    document.addEventListener("mouseup", stopResizeBottom);
    document.body.style.userSelect = "none";
    document.body.style.cursor = "ns-resize";
  };
  const doResizeTop = (e: MouseEvent) => {
    const deltaY = e.clientY - startY.value;
    const deltaMinutes = deltaY;
    let newStartMargin = startPosition.value + deltaMinutes;
    let newHeight = startHeight.value - deltaMinutes;

    if (newHeight < MIN_HEIGHT) {
      const adjustment = MIN_HEIGHT - newHeight;
      newHeight = MIN_HEIGHT;
      newStartMargin -= adjustment;
    }

    newStartMargin = Math.max(0, Math.min(1440 - newHeight, newStartMargin));
    startMargin.value =
      Math.round(newStartMargin / SNAP_INTERVAL_MINUTES) *
      SNAP_INTERVAL_MINUTES;
    timeSlotHeight.value =
      Math.round(newHeight / SNAP_INTERVAL_MINUTES) * SNAP_INTERVAL_MINUTES;
  };

  const doResizeBottom = (e: MouseEvent) => {
    const deltaY = e.clientY - startY.value;
    const deltaMinutes = deltaY;
    let newHeight = startHeight.value + deltaMinutes;
    newHeight = Math.max(MIN_HEIGHT, Math.min(ONE_DAY, newHeight));
    timeSlotHeight.value =
      Math.round(newHeight / SNAP_INTERVAL_MINUTES) * SNAP_INTERVAL_MINUTES;
  };

  const stopResizeTop = () => {
    document.removeEventListener("mousemove", doResizeTop);
    document.removeEventListener("mouseup", stopResizeTop);
    document.body.style.userSelect = "";
    document.body.style.cursor = "";
    onResizeEnd?.();
  };

  const stopResizeBottom = () => {
    document.removeEventListener("mousemove", doResizeBottom);
    document.removeEventListener("mouseup", stopResizeBottom);
    document.body.style.userSelect = "";
    document.body.style.cursor = "";
    onResizeEnd?.();
  };

  const currentDayIndex = computed(() => {
    // Number of columns moved from original day
    return Math.round(left.value / snapX);
  });

  const actualStartTime = computed(() => {
    const newStart = new Date(midnight);
    newStart.setMinutes(startMargin.value);
    // Adjust by how many days horizontally dragged
    newStart.setDate(newStart.getDate() + currentDayIndex.value);
    return newStart;
  });

  const actualEndTime = computed(() => {
    const newEnd = new Date(actualStartTime.value);
    newEnd.setMinutes(newEnd.getMinutes() + timeSlotHeight.value);
    return newEnd;
  });

  const timeRange = computed(() => {
    const formatTime = (date: Date) =>
      date.toLocaleTimeString([], {
        hour: "numeric",
        minute: "2-digit",
        hour12: true,
      });

    return `${formatTime(actualStartTime.value)} - ${formatTime(actualEndTime.value)}`;
  });

  // If start time (drag side-to-side) or time range (resize) changes don't show the edit modal
  watch(
    [actualStartTime, timeRange],
    ([newStartTime, newTimeRange], [oldStartTime, oldTimeRange]) => {
      if (newStartTime !== oldStartTime || newTimeRange !== oldTimeRange) {
        dragged.value = true;
      }
    },
  );

  // Clean up listeners if they somehow still exist
  onUnmounted(() => {
    document.removeEventListener("mousemove", doResizeBottom);
    document.removeEventListener("mouseup", stopResizeTop);
    document.removeEventListener("mousemove", doResizeTop);
    document.removeEventListener("mouseup", stopResizeBottom);
    document.removeEventListener("mousemove", onDrag);
    document.removeEventListener("mouseup", stopDrag);
  });

  return {
    timeSlotHeight,
    startMargin,
    currentDayIndex,
    timeRange,
    dragged,
    actualStartTime,
    actualEndTime,
    HOUR_HEIGHT,
    startResizeTop,
    startResizeBottom,
    startDrag,
  };
}
