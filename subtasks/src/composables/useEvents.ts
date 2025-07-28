import { toValue, type MaybeRefOrGetter } from "vue";
import {
  keepPreviousData,
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/vue-query";
import type { Event, EventResponse } from "@annotations/event";
import { useToast } from "primevue";

async function getEvents({
  startTime,
  endTime,
}: {
  startTime: Date;
  endTime: Date;
}): Promise<EventResponse[]> {
  const res = await fetch(
    `http://localhost:8000/events?start_at=${startTime.toISOString()}&end_at=${endTime.toISOString()}`,
    {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
    },
  );

  if (!res.ok) {
    throw new Error("Could not get events");
  }
  return res.json();
}

async function updateEvent({
  event,
  eventId,
}: {
  event: Event;
  eventId: number;
}): Promise<Event> {
  const res = await fetch(`http://localhost:8000/event/${eventId}`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: JSON.stringify(event),
  });

  if (!res.ok) {
    throw new Error("Could not update event");
  }
  return res.json();
}

async function createEvent({ event }: { event: Event }): Promise<Event> {
  const res = await fetch(`http://localhost:8000/event`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: JSON.stringify(event),
  });

  if (!res.ok) {
    throw new Error("Could not create new event");
  }
  return res.json();
}

async function deleteEvent({
  eventId: eventId,
}: {
  eventId: number;
}): Promise<number> {
  const res = await fetch(`http://localhost:8000/event${eventId}`, {
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

export function useEvents({
  startTime,
  endTime,
}: {
  startTime: MaybeRefOrGetter<Date>;
  endTime: MaybeRefOrGetter<Date>;
}) {
  return useQuery({
    placeholderData: keepPreviousData,
    queryKey: ["events", startTime, endTime],
    queryFn: () =>
      getEvents({
        startTime: toValue(startTime),
        endTime: toValue(endTime),
      }),
  });
}

export function useCreateEvent() {
  const queryClient = useQueryClient();
  const toast = useToast();
  return useMutation({
    mutationFn: ({ event }: { event: Event }) =>
      createEvent({
        event,
      }),
    onSuccess: (event) => {
      queryClient.invalidateQueries({ queryKey: ["events"] });
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
      queryClient.invalidateQueries({ queryKey: ["events"] });
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
      queryClient.invalidateQueries({ queryKey: ["events"] });
      toast.add({ detail: `Delete event` });
    },
  });
}
