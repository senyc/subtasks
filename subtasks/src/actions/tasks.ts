import type Task from "@annotations/task";
import { calculateOffsetLimit } from "../utils/pagination";

export async function getTasks({
  projectId,
  completed,
  page,
  pageSize,
}: {
  projectId: number;
  completed: boolean;
  page: number;
  pageSize: number;
}): Promise<Task[]> {
  const [offset, limit] = calculateOffsetLimit({
    page: page,
    pageSize: pageSize,
  });
  const res = await fetch(
    `http://localhost:8000/project/${projectId}/tasks${completed ? "/completed" : ""}?offset=${offset}&limit=${limit}`,
  );
  if (!res.ok) {
    throw new Error("Cannot fetch tasks");
  }
  return res.json();
}
