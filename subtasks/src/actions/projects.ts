import { keepPreviousData, useQuery } from "@tanstack/vue-query";
import type { ProjectResponse } from "../annotations/project";

function calculateOffsetLimit({
  page,
  pageSize,
}: {
  /** This value is expected to be one indexed*/
  page: number;
  pageSize: number;
}) {
  const offset = (page - 1) * pageSize;
  const limit = page * pageSize;
  /** These values are expected to be 0-indexed as they are used in the query*/
  return [offset, limit];
}

async function getProjects({
  completed,
  page,
  pageSize,
}: {
  completed: boolean;
  page: number;
  pageSize: number;
}): Promise<{ projects: ProjectResponse[]; count: number }> {
  const [offset, limit] = calculateOffsetLimit({
    page: page,
    pageSize: pageSize,
  });

  const res = await fetch(
    `http://localhost:8000/projects${completed ? "/completed" : ""}?offset=${offset}&limt=${limit}`,
  );
  if (!res.ok) {
    throw new Error("Cannot fetch projects");
  }
  return res.json();
}

export default ({
  completed = false,
  page,
  pageSize = 20,
}: {
  completed?: boolean;
  page: number;
  pageSize?: number;
}) =>
  useQuery({
    placeholderData: keepPreviousData,
    queryKey: [
      "projects",
      completed ? "completed" : "incomplete",
      page,
      pageSize,
    ],
    queryFn: () =>
      getProjects({ pageSize: pageSize, page: page, completed: completed }),
  });
