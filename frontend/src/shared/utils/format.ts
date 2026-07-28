export function formatSalary(min: number | null, max: number | null): string {
  const format = (n: number) => `₹${(n / 100000).toFixed(0)}L`
  if (min && max) return `${format(min)} – ${format(max)} / yr`
  if (min) return `From ${format(min)} / yr`
  if (max) return `Up to ${format(max)} / yr`
  return 'Salary not disclosed'
}

export function formatEmploymentType(type: string): string {
  return type.replace('_', '-').replace(/\b\w/g, (c) => c.toUpperCase())
}

export function formatRelativeDate(iso: string): string {
  const date = new Date(iso)
  const diffMs = Date.now() - date.getTime()
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24))
  if (diffDays <= 0) return 'Today'
  if (diffDays === 1) return 'Yesterday'
  if (diffDays < 30) return `${diffDays}d ago`
  return date.toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })
}
