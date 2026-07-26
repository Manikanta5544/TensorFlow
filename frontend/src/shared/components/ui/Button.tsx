import { clsx } from "clsx";
import type { ButtonHTMLAttributes } from "react";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "ghost" | "danger";
  size?: "sm" | "md";
  isLoading?: boolean;
}

export function Button({
  variant = "primary",
  size = "md",
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
        "inline-flex items-center justify-center gap-2 rounded-full font-medium transition-colors duration-150",
        "disabled:cursor-not-allowed disabled:opacity-60",
        size === "md" ? "px-5 py-2.5 text-sm" : "px-3.5 py-1.5 text-sm",
        variant === "primary" && "bg-ink text-paper hover:bg-accent",
        variant === "secondary" && "bg-white text-ink border border-border hover:border-ink",
        variant === "ghost" && "text-ink hover:bg-black/5",
        variant === "danger" && "bg-danger text-white hover:bg-danger/90",
        className,
      )}
      {...props}
    >
      {isLoading && (
        <span className="h-3.5 w-3.5 animate-spin rounded-full border-2 border-current border-t-transparent" />
      )}
      {children}
    </button>
  );
}
