import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Navigate, Route, BrowserRouter, Routes } from 'react-router-dom'
import { AuthProvider, useAuth } from '@/features/auth/auth-context'
import { LoginPage } from '@/features/auth/components/LoginPage'
import { RegisterPage } from '@/features/auth/components/RegisterPage'
import { CandidateDashboard } from '@/features/dashboard/components/CandidateDashboard'
import { RecruiterDashboard } from '@/features/dashboard/components/RecruiterDashboard'
import { JobDetailPage } from '@/features/jobs/components/JobDetailPage'
import { JobsListPage } from '@/features/jobs/components/JobsListPage'
import { PostJobPage } from '@/features/jobs/components/PostJobPage'
import { Navbar } from '@/shared/components/Navbar'
import { ProtectedRoute } from '@/shared/components/ProtectedRoute'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { retry: 1, staleTime: 30_000 },
  },
})

function DashboardRouter() {
  const { user } = useAuth()
  if (user?.role === 'recruiter') return <RecruiterDashboard />
  return <CandidateDashboard />
}

function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/jobs" replace />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/jobs" element={<JobsListPage />} />
      <Route path="/jobs/:jobId" element={<JobDetailPage />} />
      <Route
        path="/post-job"
        element={
          <ProtectedRoute role="recruiter">
            <PostJobPage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <DashboardRouter />
          </ProtectedRoute>
        }
      />
      <Route path="*" element={<Navigate to="/jobs" replace />} />
    </Routes>
  )
}

export function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <BrowserRouter>
          <Navbar />
          <AppRoutes />
        </BrowserRouter>
      </AuthProvider>
    </QueryClientProvider>
  )
}
