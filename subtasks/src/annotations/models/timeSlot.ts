
/** Response from the getter */
export interface TimeSlotResponse {
  id: number;
  type: 'event' | 'task'
  is_recurring: boolean;
  title: string;
  start_at: string;
  end_at: string;
  notes?: string;
}

/** Data passed to the setter */
export interface TimeSlot {
  type: 'event' | 'task'
  is_recurring?: boolean;
  title?: string;
  start_at?: Date;
  end_at?: Date;
  notes?: string;
}

/** This is the data used in the form intermediary */
export interface TimeSlotForm {
  type: 'event' | 'task'
  is_recurring?: boolean;
  title: string;
  /** Should be IsoString*/
  start_at: string;
  /** Should be IsoString*/
  end_at: string;
  notes?: string;
}
