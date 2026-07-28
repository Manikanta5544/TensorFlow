import { zodResolver } from '@hookform/resolvers/zod'
import { useMutation } from '@tanstack/react-query'
import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { Link, useNavigate } from 'react-router-dom'
import { registerRequest } from '@/features/auth/api/auth-api'
import { useAuth } from '@/features/auth/auth-context'
import { registerSchema, type RegisterFormValues } from '@/features/auth/types/schemas'
import { Button } from '@/shared/components/ui/Button'
import { TextField } from '@/shared/components/ui/TextField'
import { getApiErrorMessage } from '@/shared/lib/api-client'
import { clsx } from 'clsx'

export function RegisterPage() {
  const navigate = useNavigate()
  const { login } = useAuth()
  const [role, setRole] = useState<'candidate' | 'recruiter'>('candidate')

  const {
    register,
    handleSubmit,
    setValue,
    formState: { errors },
  } = useForm<RegisterFormValues>({
    resolver: zodResolver(registerSchema),
    defaultValues: { role: 'candidate' },
  })

  const mutation = useMutation({
    mutationFn: registerRequest,
    onSuccess: (data) => {
      login(data.access_token, data.user)
      navigate(data.user.role === 'recruiter' ? '/dashboard' : '/jobs')
    },
  })

  function handleRoleChange(next: 'candidate' | 'recruiter') {
    setRole(next)
    setValue('role', next)
  }

  return (
    <div className="mx-auto flex min-h-[calc(100vh-64px)] max-w-md flex-col justify-center px-6 py-16">
      <h1 className="font-display text-3xl text-ink">Create your account</h1>
      <p className="mt-2 text-sm text-muted">
        Join as a recruiter to post jobs, or a candidate to apply.
      </p>

      <div className="mt-6 grid grid-cols-2 gap-2 rounded-full border border-border bg-white p-1">
        {(['candidate', 'recruiter'] as const).map((option) => (
          <button
            key={option}
            type="button"
            onClick={() => handleRoleChange(option)}
            className={clsx(
              'rounded-full py-2 text-sm font-medium capitalize transition-colors',
              role === option ? 'bg-ink text-paper' : 'text-muted hover:text-ink',
            )}
          >
            {option}
          </button>
        ))}
      </div>

      <form
        onSubmit={handleSubmit((values) => mutation.mutate(values))}
        className="mt-6 flex flex-col gap-4"
      >
        <TextField
          label="Full name"
          autoComplete="name"
          error={errors.full_name?.message}
          {...register('full_name')}
        />
        <TextField
          label="Email"
          type="email"
          autoComplete="email"
          error={errors.email?.message}
          {...register('email')}
        />
        {role === 'recruiter' && (
          <TextField
            label="Company name"
            error={errors.company_name?.message}
            {...register('company_name')}
          />
        )}
        <TextField
          label="Password"
          type="password"
          autoComplete="new-password"
          hint="At least 8 characters, one uppercase letter, one number."
          error={errors.password?.message}
          {...register('password')}
        />

        {mutation.isError && (
          <p className="rounded-lg bg-danger-soft px-3.5 py-2.5 text-sm text-danger">
            {getApiErrorMessage(mutation.error, 'Unable to create your account.')}
          </p>
        )}

        <Button type="submit" isLoading={mutation.isPending} className="mt-2 w-full">
          Create account
        </Button>
      </form>

      <p className="mt-6 text-center text-sm text-muted">
        Already have an account?{' '}
        <Link to="/login" className="font-medium text-accent hover:underline">
          Sign in
        </Link>
      </p>
    </div>
  )
}
