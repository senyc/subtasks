export default interface Task {
  title: string;
  body: string;
  id: number;
  project_id?: number;
  due_date?: string
  completed_date?: string
  created_at?: string
}
