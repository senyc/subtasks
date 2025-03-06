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

async function getTasks(projectId: number): Promise<Task[]> {
  const res = await fetch(`http://localhost:8000/project/${projectId}/tasks`);
  if (!res.ok) {
    throw new Error("Cannot fetch tasks");
  }
  return res.json();
}

export default ({
  projectId,
  showCompleted,
}: {
  projectId: number;
  showCompleted: boolean;
}) =>
  useQuery({
    queryKey: ["tasks", projectId, showCompleted ? "completed" : "incompleted"],
    queryFn: () => {
      return showCompleted ? getCompletedTasks(projectId) : getTasks(projectId);
    },
  });
