import type { Delta } from "@vueup/vue-quill";
import type { Tag } from "../tag";

/** Response from the getter */
export interface TaskResponse {
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
  tags?: Tag[];
}

/** Data passed to the setter */
export interface Task {
  title: string;
  body?: string;
  do_date?: Date
  project_id?: number;
  completed_date?: string;
  time_estimate?: number;
  tags?: Tag[];
}

/** This is the data used in the form intermediary */
export interface TaskForm {
  title: string;
  body: Delta;
  project_id?: number;
  due_date?: string;
  completed_date?: string;
  time_estimate?: number;
  tags?: Tag[];
}
