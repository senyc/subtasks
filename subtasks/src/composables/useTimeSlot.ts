import {
  useMutation,
  useQueryClient,
} from "@tanstack/vue-query";
import type { Event } from "@annotations/event";
import { useToast } from "primevue";
import type { TimeSlot } from "@annotations/models/timeSlot";

// TODO: create a get timeslot function and hook (probably include a type like task/event)
async function updateTimeSlot({
  timeSlot,
  eventId,
}: {
  timeSlot: TimeSlot;
  eventId: number;
}): Promise<Event> {
  const res = await fetch(`http://localhost:8000/event/${eventId}`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: JSON.stringify(timeSlot),
  });

  if (!res.ok) {
    throw new Error("Could not update event");
  }
  return res.json();
}

async function createTimeSlot({ timeSlot }: { timeSlot: TimeSlot }): Promise<TimeSlot> {
  const res = await fetch(`http://localhost:8000/event`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: JSON.stringify(timeSlot),
  });

  if (!res.ok) {
    throw new Error("Could not create new event");
  }
  return res.json();
}

async function deleteTimeSlot({
  eventId: eventId,
}: {
  eventId: number;
}): Promise<number> {
  const res = await fetch(`http://localhost:8000/event/${eventId}`, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
  });

  if (!res.ok) {
    throw new Error("Could not delete event");
  }
  return res.json();
}

export function useCreateTimeSlot() {
  const queryClient = useQueryClient();
  const toast = useToast();
  return useMutation({
    mutationFn: ({ event }: { event: TimeSlot }) =>
      createTimeSlot({
        timeSlot: event,
      }),
    onSuccess: (event) => {
      queryClient.invalidateQueries({ queryKey: ["calendar"] });
      toast.add({
        severity: "success",
        summary: "Event",
        detail: `Created ${event.title}`,
        life: 2000,
      });
    },
  });
}

export function useUpdateTimeSlot() {
  const queryClient = useQueryClient();
  const toast = useToast();
  return useMutation({
    mutationFn: ({ timeSlot, eventId }: { timeSlot: TimeSlot; eventId: number }) =>
      updateTimeSlot({
        timeSlot,
        eventId,
      }),
    onSuccess: (event) => {
      queryClient.invalidateQueries({ queryKey: ["calendar"] });
      toast.add({
        severity: "success",
        summary: "Event",
        detail: `Updated ${event.title}`,
        life: 2000,
      });
    },
  });
}

export function useDeleteTimeSlot() {
  const queryClient = useQueryClient();
  const toast = useToast();
  return useMutation({
    mutationFn: ({ eventId: eventId }: { eventId: number }) =>
      deleteTimeSlot({
        eventId,
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["calendar"] });
      toast.add({
        severity: "success",
        summary: "Event",
        detail: `Delete event`,
        life: 2000,
      });
    },
  });
}
