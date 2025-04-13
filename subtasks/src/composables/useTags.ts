import { toValue, type MaybeRefOrGetter } from "vue";
import { keepPreviousData, useQuery } from "@tanstack/vue-query";
import type { Tag } from "@annotations/tag";

async function getTags({
  type,
  search,
}: {
  type: "projects" | "tasks";
  search: string;
}): Promise<Tag[]> {
  const res = await fetch(
    `http://localhost:8000/tags/${type}?offset=${0}&limit=${5}&search=${search}`,
  );
  if (!res.ok) {
    throw new Error("Cannot fetch tags");
  }

  return res.json();
}

export function useTags({
  type,
  search = "",
}: {
  type: "projects" | "tasks";
  search?: MaybeRefOrGetter<string>;
}) {
  return useQuery({
    placeholderData: keepPreviousData,
    queryKey: ["tags", type, search],

    queryFn: () =>
      getTags({
        type: type,
        search: toValue(search),
      }),
  });
}
