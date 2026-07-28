import { clsx } from 'clsx'
import { Link, NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '@/features/auth/auth-context'
import { Button } from '@/shared/components/ui/Button'

const navLinkClass = ({ isActive }: { isActive: boolean }) =>
  clsx(
    'text-sm transition-colors',
    isActive ? 'text-ink' : 'text-ink/60 hover:text-ink',
  )

export function Navbar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  function handleLogout() {
    logout()
    navigate('/login')
  }

  return (
    <header className="sticky top-0 z-40 border-b border-border bg-paper/90 backdrop-blur">
      <nav className="mx-auto flex max-w-5xl items-center justify-between px-6 py-4">
        <Link to="/jobs" className="flex items-center gap-2.5">
          <span className="flex h-7 w-7 items-center justify-center rounded-md bg-ink font-display text-sm text-paper">
            T
          </span>
          <span className="font-display text-[17px] leading-none text-ink">
            TensorFlow<span className="text-accent"> AI</span>
          </span>
        </Link>

        <div className="flex items-center gap-6">
          <NavLink to="/jobs" className={navLinkClass}>
            Browse jobs
          </NavLink>

          {user?.role === 'recruiter' && (
            <>
              <NavLink to="/dashboard" className={navLinkClass}>
                Dashboard
              </NavLink>
              <NavLink to="/post-job" className={navLinkClass}>
                Post a job
              </NavLink>
            </>
          )}
          {user?.role === 'candidate' && (
            <NavLink to="/dashboard" className={navLinkClass}>
              My applications
            </NavLink>
          )}

          {user ? (
            <div className="flex items-center gap-3 border-l border-border pl-5">
              <span className="hidden text-sm text-muted sm:inline">{user.full_name}</span>
              <Button variant="secondary" size="sm" onClick={handleLogout}>
                Sign out
              </Button>
            </div>
          ) : (
            <div className="flex items-center gap-2 border-l border-border pl-5">
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
  )
}