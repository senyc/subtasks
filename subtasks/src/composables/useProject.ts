import { useQuery } from "@tanstack/vue-query";
import type { Project } from "../annotations/project";

async function getProject(id: number): Promise<Project> {
  const res = await fetch(`http://localhost:8000/project/${id}`);
  if (!res.ok) {
    throw new Error("Cannot fetch project");
  }
  return res.json();
}

export default function useProject({
  id,
  enabled = true,
}: {
  id: number;
  enabled?: boolean;
}) {
  return useQuery({
    enabled: enabled,
    queryKey: ["project", id],
    queryFn: () => getProject(id),
  });
}
