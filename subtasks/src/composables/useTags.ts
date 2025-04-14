import { toValue, type MaybeRefOrGetter } from "vue";
import { keepPreviousData, useQuery } from "@tanstack/vue-query";
import type { Tag } from "@annotations/tag";

async function getTags({
  type,
  search,
  limit,
  offset,
}: {
  type: "projects" | "tasks";
  search: string;
  limit: number;
  offset: number;
}): Promise<Tag[]> {
  const res = await fetch(
    `http://localhost:8000/tags/${type}?offset=${offset}&limit=${limit}&search=${search}`,
  );
  if (!res.ok) {
    throw new Error("Cannot fetch tags");
  }

  return res.json();
}

export default function useTags({
  type,
  search = "",
  limit = 5,
  offset = 0,
  enabled = false,
}: {
  type: "projects" | "tasks";
  search?: MaybeRefOrGetter<string>;
  limit?: number;
  offset?: number;
  enabled?: MaybeRefOrGetter<boolean>;
}) {
  return useQuery({
    placeholderData: keepPreviousData,
    queryKey: ["tags", type, search],
    enabled,
    queryFn: () =>
      getTags({
        offset,
        limit,
        type,
        search: toValue(search),
      }),
  });
}
