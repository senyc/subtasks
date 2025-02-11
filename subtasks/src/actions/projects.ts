import { useQuery } from '@tanstack/vue-query'
import type { ProjectResponse } from '../annotations/project'

async function getProjects(): Promise<ProjectResponse[]> {
  const res = await fetch("http://localhost:8000/projects")
  if (!res.ok) {
    throw new Error("Cannot fetch projects")
  }
  return res.json()
}

export default () => useQuery({ queryKey: ['projects'], queryFn: getProjects })
