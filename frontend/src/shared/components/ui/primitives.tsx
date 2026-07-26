import { clsx } from "clsx";
import { forwardRef, type SelectHTMLAttributes } from "react";

interface SelectFieldProps extends SelectHTMLAttributes<HTMLSelectElement> {
  label: string;
  error?: string;
}

export const SelectField = forwardRef<HTMLSelectElement, SelectFieldProps>(
  ({ label, error, id, className, children, ...props }, ref) => {
    const fieldId = id ?? props.name ?? label;
    return (
      <div className="flex flex-col gap-1.5">
        <label htmlFor={fieldId} className="text-sm font-medium text-ink">
          {label}
        </label>
        <select
          ref={ref}
          id={fieldId}
          className={clsx(
            "rounded-lg border bg-white px-3.5 py-2.5 text-sm text-ink",
            "focus:outline-none focus:ring-2 focus:ring-accent/40 focus:border-accent",
            error ? "border-danger" : "border-border",
            className,
          )}
          {...props}
        >
          {children}
        </select>
        {error && <p className="text-xs text-danger">{error}</p>}
      </div>
    );
  },
);
SelectField.displayName = "SelectField";

export function Card({ className, children }: { className?: string; children: React.ReactNode }) {
  return (
    <div className={clsx("rounded-card border border-border bg-white shadow-card", className)}>
      {children}
    </div>
  );
}

const statusStyles: Record<string, string> = {
  submitted: "bg-accent-soft text-accent",
  reviewed: "bg-amber-100 text-amber-800",
  accepted: "bg-success-soft text-success",
  rejected: "bg-danger-soft text-danger",
  open: "bg-success-soft text-success",
  closed: "bg-black/5 text-muted",
};

export function Badge({ status, children }: { status: string; children: React.ReactNode }) {
  return (
    <span
      className={clsx(
        "inline-flex items-center rounded-full px-2.5 py-1 text-xs font-medium capitalize",
        statusStyles[status] ?? "bg-black/5 text-muted",
      )}
    >
      {children}
    </span>
  );
}

export function Spinner({ className }: { className?: string }) {
  return (
    <span
      role="status"
      aria-label="Loading"
      className={clsx(
        "inline-block h-5 w-5 animate-spin rounded-full border-2 border-ink/20 border-t-ink",
        className,
      )}
    />
  );
}

export function EmptyState({ title, description }: { title: string; description: string }) {
  return (
    <div className="flex flex-col items-center gap-1.5 rounded-card border border-dashed border-border py-16 text-center">
      <p className="font-display text-lg text-ink">{title}</p>
      <p className="max-w-sm text-sm text-muted">{description}</p>
    </div>
  );
}
