import { clsx } from 'clsx'
import { forwardRef, type InputHTMLAttributes, type TextareaHTMLAttributes } from 'react'

interface FieldWrapperProps {
  label: string
  error?: string
  hint?: string
  htmlFor: string
  children: React.ReactNode
}

function FieldWrapper({ label, error, hint, htmlFor, children }: FieldWrapperProps) {
  return (
    <div className="flex flex-col gap-1.5">
      <label htmlFor={htmlFor} className="caption-label">
        {label}
      </label>
      {children}
      {hint && !error && <p className="text-xs text-muted">{hint}</p>}
      {error && <p className="text-xs text-danger">{error}</p>}
    </div>
  )
}

interface TextFieldProps extends InputHTMLAttributes<HTMLInputElement> {
  label: string
  error?: string
  hint?: string
}

export const TextField = forwardRef<HTMLInputElement, TextFieldProps>(
  ({ label, error, hint, id, className, ...props }, ref) => {
    const fieldId = id ?? props.name ?? label
    return (
      <FieldWrapper label={label} error={error} hint={hint} htmlFor={fieldId}>
        <input
          ref={ref}
          id={fieldId}
          className={clsx(
            'rounded-lg border bg-white px-3.5 py-2.5 text-sm text-ink placeholder:text-muted/70',
            'transition-colors duration-150 focus:border-accent focus:outline-none focus:ring-2 focus:ring-accent/20',
            error ? 'border-danger' : 'border-border',
            className,
          )}
          {...props}
        />
      </FieldWrapper>
    )
  },
)
TextField.displayName = 'TextField'

interface TextAreaFieldProps extends TextareaHTMLAttributes<HTMLTextAreaElement> {
  label: string
  error?: string
  hint?: string
}

export const TextAreaField = forwardRef<HTMLTextAreaElement, TextAreaFieldProps>(
  ({ label, error, hint, id, className, ...props }, ref) => {
    const fieldId = id ?? props.name ?? label
    return (
      <FieldWrapper label={label} error={error} hint={hint} htmlFor={fieldId}>
        <textarea
          ref={ref}
          id={fieldId}
          className={clsx(
            'rounded-lg border bg-white px-3.5 py-2.5 text-sm text-ink placeholder:text-muted/70',
            'transition-colors duration-150 focus:border-accent focus:outline-none focus:ring-2 focus:ring-accent/20',
            error ? 'border-danger' : 'border-border',
            className,
          )}
          {...props}
        />
      </FieldWrapper>
    )
  },
)
TextAreaField.displayName = 'TextAreaField'
