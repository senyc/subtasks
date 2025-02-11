export interface Project {
  title: string;
  due?: string;
  body?: string;
  id: number;
}

export interface ProjectResponse extends Project {
  total_tasks: number;
  completed_tasks: number;
}
