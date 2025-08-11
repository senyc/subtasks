import { useMutation, useQueryClient } from "@tanstack/vue-query";
import type { Event, EventResponse } from "@annotations/models/event";
import { useToast } from "primevue";

// TODO: add use event hook
async function updateEvent({
  event: timeSlot,
  eventId,
}: {
  event: Event;
  eventId: number;
}): Promise<EventResponse> {
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

async function createEvent({
  timeSlot,
}: {
  timeSlot: Event;
}): Promise<EventResponse> {
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
type EventId = number;
async function deleteEvent({
  eventId: eventId,
}: {
  eventId: number;
}): Promise<EventId> {
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

export function useCreateEvent() {
  const queryClient = useQueryClient();
  const toast = useToast();
  return useMutation({
    mutationFn: ({ event }: { event: Event }) =>
      createEvent({
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

export function useUpdateEvent() {
  const queryClient = useQueryClient();
  const toast = useToast();
  return useMutation({
    mutationFn: ({ event, eventId }: { event: Event; eventId: number }) =>
      updateEvent({
        event,
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

export function useDeleteEvent() {
  const queryClient = useQueryClient();
  const toast = useToast();
  return useMutation({
    mutationFn: ({ eventId: eventId }: { eventId: number }) =>
      deleteEvent({
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
