import type { ProjectResponse } from "../annotations/project";
import { calculateOffsetLimit } from "../utils/pagination";

export async function getProjects({
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
