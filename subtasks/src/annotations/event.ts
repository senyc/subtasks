export interface Event {
  is_recurring?: boolean;
  title?: string;
  start_at?: Date;
  end_at?: Date;
  notes?: string;
}

export interface EventResponse {
  id: number;
  is_recurring: boolean;
  title: string;
  start_at: string;
  end_at: string;
  notes?: string;
}
