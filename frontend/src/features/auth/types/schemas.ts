import { z } from 'zod'

export const loginSchema = z.object({
  email: z.string().min(1, 'Email is required').email('Enter a valid email address'),
  password: z.string().min(1, 'Password is required'),
})
export type LoginFormValues = z.infer<typeof loginSchema>

export const registerSchema = z
  .object({
    full_name: z.string().min(2, 'Enter your full name'),
    email: z.string().min(1, 'Email is required').email('Enter a valid email address'),
    password: z
      .string()
      .min(8, 'Password must be at least 8 characters')
      .regex(/[A-Z]/, 'Include at least one uppercase letter')
      .regex(/[0-9]/, 'Include at least one number'),
    role: z.enum(['recruiter', 'candidate']),
    company_name: z.string().optional(),
  })
  .refine((data) => data.role !== 'recruiter' || !!data.company_name?.trim(), {
    message: 'Company name is required for recruiter accounts',
    path: ['company_name'],
  })
export type RegisterFormValues = z.infer<typeof registerSchema>
