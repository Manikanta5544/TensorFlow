import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "@/features/auth/auth-context";
import { Button } from "@/shared/components/ui/Button";

export function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate("/login");
  }

  return (
    <header className="sticky top-0 z-40 border-b border-border bg-paper/90 backdrop-blur">
      <nav className="mx-auto flex max-w-5xl items-center justify-between px-6 py-4">
        <Link to="/jobs" className="flex items-center gap-2">
          <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-accent text-sm font-bold text-white">
            T
          </span>
          <span className="font-display text-lg text-ink">TalentFlow AI</span>
        </Link>

        <div className="flex items-center gap-5">
          <Link to="/jobs" className="text-sm text-ink/80 hover:text-ink">
            Browse jobs
          </Link>

          {user?.role === "recruiter" && (
            <>
              <Link to="/dashboard" className="text-sm text-ink/80 hover:text-ink">
                Dashboard
              </Link>
              <Link to="/post-job" className="text-sm text-ink/80 hover:text-ink">
                Post a job
              </Link>
            </>
          )}
          {user?.role === "candidate" && (
            <Link to="/dashboard" className="text-sm text-ink/80 hover:text-ink">
              My applications
            </Link>
          )}

          {user ? (
            <div className="flex items-center gap-3">
              <span className="hidden text-sm text-muted sm:inline">{user.full_name}</span>
              <Button variant="secondary" size="sm" onClick={handleLogout}>
                Sign out
              </Button>
            </div>
          ) : (
            <div className="flex items-center gap-2">
              <Link to="/login">
                <Button variant="ghost" size="sm">
                  Sign in
                </Button>
              </Link>
              <Link to="/register">
                <Button size="sm">Get started</Button>
              </Link>
            </div>
          )}
        </div>
      </nav>
    </header>
  );
}
