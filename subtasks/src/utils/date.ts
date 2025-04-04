export function reprDate(date?: string): string {
    if (!date) {
        return ""
        }

  return new Date(date).toLocaleString('default', {
    day: 'numeric',
    month: 'long'
  })
}

export function dateHasElapsed(inputDate: Date) {
  const today = new Date();

  inputDate.setHours(0, 0, 0, 0);
  today.setHours(0, 0, 0, 0);

  return inputDate < today;
}

export function dateIsToday(inputDate: Date) {
  const today = new Date();

  inputDate.setHours(0, 0, 0, 0);
  today.setHours(0, 0, 0, 0);

  return inputDate.getTime() === today.getTime();
}
