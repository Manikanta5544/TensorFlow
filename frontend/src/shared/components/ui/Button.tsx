import { clsx } from 'clsx'
import type { ButtonHTMLAttributes } from 'react'

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger'
  size?: 'sm' | 'md'
  isLoading?: boolean
}

export function Button({
  variant = 'primary',
  size = 'md',
  isLoading = false,
  disabled,
  className,
  children,
  ...props
}: ButtonProps) {
  return (
    <button
      disabled={disabled || isLoading}
      className={clsx(
        'inline-flex items-center justify-center gap-2 rounded-lg font-medium tracking-[-0.005em]',
        'transition-[background-color,border-color,color,transform] duration-150 active:scale-[0.98]',
        'disabled:cursor-not-allowed disabled:opacity-60 disabled:active:scale-100',
        size === 'md' ? 'px-4 py-2.5 text-sm' : 'px-3 py-1.5 text-[13px]',
        variant === 'primary' &&
          'bg-ink text-paper shadow-[0_1px_0_rgba(255,255,255,0.06)_inset] hover:bg-accent',
        variant === 'secondary' &&
          'border border-border bg-white text-ink hover:border-ink/30 hover:bg-ink/[0.03]',
        variant === 'ghost' && 'text-ink/80 hover:bg-ink/[0.05] hover:text-ink',
        variant === 'danger' && 'bg-danger text-white hover:bg-danger/90',
        className,
      )}
      {...props}
    >
      {isLoading && (
        <span className="h-3.5 w-3.5 animate-spin rounded-full border-2 border-current border-t-transparent" />
      )}
      {children}
    </button>
  )
}
