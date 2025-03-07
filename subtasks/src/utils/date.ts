export function reprDate(date?: string): string {
    if (!date) {
        return ""
        }

  return new Date(date).toLocaleString('default', {
    day: 'numeric',
    month: 'long'
  })
}
