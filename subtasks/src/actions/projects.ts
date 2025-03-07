import { useQuery } from "@tanstack/vue-query";
import type { ProjectResponse } from "../annotations/project";

async function getProjects(completed: boolean): Promise<ProjectResponse[]> {
  const res = await fetch(
    `http://localhost:8000/projects${completed ? "/completed" : ""}`,
  );
  if (!res.ok) {
    throw new Error("Cannot fetch projects");
  }
  return res.json();
}

export default ({ completed = false }: { completed?: boolean }) =>
  useQuery({
    queryKey: ["projects", completed ? "completed" : "incomplete"],
    queryFn: () => getProjects(completed),
  });
