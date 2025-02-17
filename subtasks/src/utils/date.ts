export function reprDate(date?: string): string {
    if (!date) {
        return ""
        }

  return new Date(date).toLocaleString('default', {
    timeZone: "UTC",
    day: 'numeric',
    month: 'long'
  })
}
