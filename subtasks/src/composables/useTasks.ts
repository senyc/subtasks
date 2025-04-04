import { calculateOffsetLimit } from "../utils/pagination";
import { toValue, type MaybeRefOrGetter } from "vue";
import { keepPreviousData, useQuery } from "@tanstack/vue-query";
import type { Task } from "@annotations/task";

async function getTasks({
  projectId,
  completed,
  page,
  pageSize,
  search = "",
}: {
  projectId?: number;
  completed: boolean;
  page: number;
  pageSize: number;
  search?: string;
}): Promise<{ tasks: Task[]; count: number }> {
  const [offset, limit] = calculateOffsetLimit({
    page: page,
    pageSize: pageSize,
  });
  const res = await fetch(
    `http://localhost:8000${projectId ? `/project/${projectId}` : "" }/tasks${completed ? "/completed" : ""}?offset=${offset}&limit=${limit}&search=${search}`,
  );

  if (!res.ok) {
    throw new Error("Cannot fetch tasks");
  }
  return res.json();
}

export function useTasks({
  projectId,
  completed,
  page,
  pageSize,
  search,
}: {
  projectId?: MaybeRefOrGetter<number>;
  completed: MaybeRefOrGetter<boolean>;
  search?: MaybeRefOrGetter<string>;
  page: MaybeRefOrGetter<number>;
  pageSize: MaybeRefOrGetter<number>;
}) {
  return useQuery({
    placeholderData: keepPreviousData,
    queryKey: [
      "tasks",
      // empty string for no project (all tasks)
      projectId ?? "",
      completed ? "completed" : "incompleted",
      { search: search, page: page, size: pageSize },
    ],
    queryFn: () =>
      getTasks({
        projectId: toValue(projectId),
        completed: toValue(completed),
        page: toValue(page),
        pageSize: toValue(pageSize),
        search: toValue(search),
      }),
  });
}
