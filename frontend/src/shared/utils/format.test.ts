import { describe, expect, it } from 'vitest'
import { formatEmploymentType, formatSalary } from '@/shared/utils/format'

describe('formatSalary', () => {
  it('formats a min-max range in lakhs', () => {
    expect(formatSalary(1000000, 2000000)).toBe('₹10L – ₹20L / yr')
  })

  it('formats a min-only value', () => {
    expect(formatSalary(1500000, null)).toBe('From ₹15L / yr')
  })

  it('formats a max-only value', () => {
    expect(formatSalary(null, 3000000)).toBe('Up to ₹30L / yr')
  })

  it('falls back when neither is set', () => {
    expect(formatSalary(null, null)).toBe('Salary not disclosed')
  })
})

describe('formatEmploymentType', () => {
  it('converts snake_case to Title-Case with a hyphen', () => {
    expect(formatEmploymentType('full_time')).toBe('Full-Time')
    expect(formatEmploymentType('internship')).toBe('Internship')
  })
})
