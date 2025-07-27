export default interface Event {
  id: number;
  is_recurring: boolean;
  title: string;
  start_at: Date;
  end_at: Date;
  notes?: string;
}
