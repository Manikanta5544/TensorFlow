import { Link } from "react-router-dom";
import { useMyApplications } from "@/features/applications/hooks/use-applications";
import { Badge, Card, EmptyState, Spinner } from "@/shared/components/ui/primitives";
import { Button } from "@/shared/components/ui/Button";
import { formatRelativeDate } from "@/shared/utils/format";

export function CandidateDashboard() {
  const { data: applications, isLoading } = useMyApplications();

  return (
    <div className="mx-auto max-w-3xl px-6 py-12">
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="font-display text-3xl text-ink">Your applications</h1>
          <p className="mt-1 text-sm text-muted">Track the status of every role you've applied to.</p>
        </div>
        <Link to="/jobs">
          <Button variant="secondary">Browse jobs</Button>
        </Link>
      </div>

      {isLoading ? (
        <div className="flex justify-center py-24">
          <Spinner />
        </div>
      ) : !applications || applications.length === 0 ? (
        <EmptyState title="No applications yet" description="When you apply to a job, it'll show up here." />
      ) : (
        <div className="flex flex-col gap-3">
          {applications.map((app) => (
            <Card key={app.id} className="flex items-center justify-between p-5">
              <div>
                <p className="text-sm font-medium text-ink">Application #{app.id.slice(0, 8)}</p>
                <p className="mt-0.5 text-xs text-muted">Applied {formatRelativeDate(app.created_at)}</p>
              </div>
              <Badge status={app.status}>{app.status}</Badge>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
