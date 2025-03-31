export default interface Task {
  title: string;
  body: string;
  /** Floating value, that by default will match the `id`*/
  order: number;
  id: number;
  project_id: number;
  due_date?: string
  completed_date?: string
  created_at?: string
  time_estimate?: number
}
