export interface Project {
  id: number;
  title: string;
  body?: string;
  due_date: string;
  /** Floating point, the higher the value the higher it should display on the page*/
  order: number;
  completed_date?: string;
  created_at?: string;
}

export interface ProjectResponse extends Project {
  total_tasks: number;
  completed_tasks: number;
}
