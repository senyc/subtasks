import { useQuery } from "@tanstack/vue-query";
import type Task from "@annotations/task";

async function getCompletedTasks(projectId: number): Promise<Task[]> {
  const res = await fetch(
    `http://localhost:8000/project/${projectId}/tasks/completed`,
  );
  if (!res.ok) {
    throw new Error("Cannot fetch completed tasks");
  }
  return res.json();
}

export default (projectId: number) =>
  useQuery({
    queryKey: ["tasks", projectId, "completed"],
    queryFn: () => getCompletedTasks(projectId),
  });
