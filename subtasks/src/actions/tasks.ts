import { useQuery } from "@tanstack/vue-query";
import type Task from "@annotations/task";

async function getTasks(projectId: number): Promise<Task[]> {
  const res = await fetch(`http://localhost:8000/project/${projectId}/tasks`);
  if (!res.ok) {
    throw new Error("Cannot fetch tasks");
  }
  return res.json();
}

export default (projectId: number) =>
  useQuery({ queryKey: ["tasks", projectId], queryFn: () => getTasks(projectId) });
