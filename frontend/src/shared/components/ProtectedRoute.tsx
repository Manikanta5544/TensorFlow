import type { ReactNode } from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "@/features/auth/auth-context";
import { Spinner } from "@/shared/components/ui/primitives";
import type { UserRole } from "@/shared/types";

export function ProtectedRoute({ children, role }: { children: ReactNode; role?: UserRole }) {
  const { user, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center">
        <Spinner />
      </div>
    );
  }

  if (!user) return <Navigate to="/login" replace />;
  if (role && user.role !== role) return <Navigate to="/jobs" replace />;

  return <>{children}</>;
}
