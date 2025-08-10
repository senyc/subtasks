import { toValue, type MaybeRefOrGetter } from "vue";
import {
  keepPreviousData,
  useQuery,
} from "@tanstack/vue-query";
import type { TimeSlotResponse } from "@/annotations/models/timeSlot";

async function getCalendar({
  startTime,
  endTime,
}: {
  startTime: Date;
  endTime: Date;
}): Promise<TimeSlotResponse[]> {
  const res = await fetch(
    `http://localhost:8000/calendar?start_at=${startTime.toISOString()}&end_at=${endTime.toISOString()}`,
    {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
    },
  );

  if (!res.ok) {
    throw new Error("Could not get calendar");
  }
  return res.json();
}

export function useCalendar({
  startTime,
  endTime,
}: {
  startTime: MaybeRefOrGetter<Date>;
  endTime: MaybeRefOrGetter<Date>;
}) {
  return useQuery({
    placeholderData: keepPreviousData,
    queryKey: ["calendar", startTime, endTime],
    queryFn: () =>
      getCalendar({
        startTime: toValue(startTime),
        endTime: toValue(endTime),
      }),
  });
}
