import type { Delta } from "@vueup/vue-quill";
import type { Tag } from "./tag";

export interface Task {
  title: string;
  body: string;
  /** Floating value, that by default will match the `id`*/
  order: number;
  id: number;
  project_id: number;
  due_date?: string;
  completed_date?: string;
  created_at?: string;
  time_estimate?: number;
}

export interface TaskDisplay {
  title: string;
  body: Delta;
  project_id?: number;
  due_date?: string;
  completed_date?: string;
  time_estimate?: number;
  tags?: Tag[];
}
