import { toValue, type MaybeRefOrGetter } from "vue";
import type { ProjectResponse } from "../annotations/project";
import { calculateOffsetLimit } from "../utils/pagination";
import { keepPreviousData, useQuery } from "@tanstack/vue-query";

async function getProjects({
  completed,
  page,
  pageSize,
  search,
}: {
  completed: boolean;
  page: number;
  pageSize: number;
  search: string;
}): Promise<{ projects: ProjectResponse[]; count: number }> {
  const [offset, limit] = calculateOffsetLimit({
    page: page,
    pageSize: pageSize,
  });

  const res = await fetch(
    `http://localhost:8000/projects${completed ? "/completed" : ""}?offset=${offset}&limt=${limit}&search=${search}`,
  );
  if (!res.ok) {
    throw new Error("Cannot fetch projects");
  }
  return res.json();
}

export function useProjects({
  completed,
  search = "",
  page,
  pageSize,
}: {
  completed: MaybeRefOrGetter<boolean>;
  search?: MaybeRefOrGetter<string>;
  page: MaybeRefOrGetter<number>;
  pageSize: MaybeRefOrGetter<number>;
}) {
  return useQuery({
    placeholderData: keepPreviousData,
    queryKey: [
      "projects",
      completed ? "completed" : "incomplete",
      { search: search, page: page, size: pageSize },
    ],

    queryFn: () =>
      getProjects({
        pageSize: toValue(pageSize),
        page: toValue(page),
        completed: toValue(completed),
        search: toValue(search),
      }),
  });
}
