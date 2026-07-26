import { useState } from "react";
import { Link } from "react-router-dom";
import {
  useApplicationsForJob,
  useUpdateApplicationStatus,
} from "@/features/applications/hooks/use-applications";
import { useMyJobs } from "@/features/jobs/hooks/use-jobs";
import { Badge, Card, EmptyState, Spinner } from "@/shared/components/ui/primitives";
import { Button } from "@/shared/components/ui/Button";
import type { ApplicationStatus } from "@/shared/types";
import { formatRelativeDate } from "@/shared/utils/format";

const STATUS_OPTIONS: ApplicationStatus[] = ["submitted", "reviewed", "accepted", "rejected"];

function ApplicantsPanel({ jobId }: { jobId: string }) {
  const { data: applications, isLoading } = useApplicationsForJob(jobId);
  const updateStatus = useUpdateApplicationStatus(jobId);

  if (isLoading) return <Spinner className="my-4" />;
  if (!applications || applications.length === 0) {
    return <p className="py-4 text-sm text-muted">No applications yet.</p>;
  }

  return (
    <div className="flex flex-col divide-y divide-border">
      {applications.map((app) => (
        <div key={app.id} className="flex flex-col gap-2 py-4 sm:flex-row sm:items-start sm:justify-between">
          <div className="max-w-md">
            <p className="text-sm font-medium text-ink">Applied {formatRelativeDate(app.created_at)}</p>
            {app.cover_letter && <p className="mt-1 text-sm text-ink/80">{app.cover_letter}</p>}
            <p className="mt-1 text-xs text-muted">{app.resume_text}</p>
          </div>
          <div className="flex items-center gap-2">
            <Badge status={app.status}>{app.status}</Badge>
            <select
              value={app.status}
              onChange={(e) =>
                updateStatus.mutate({ applicationId: app.id, status: e.target.value as ApplicationStatus })
              }
              className="rounded-lg border border-border bg-white px-2 py-1 text-xs focus:outline-none focus:ring-2 focus:ring-accent/40"
            >
              {STATUS_OPTIONS.map((status) => (
                <option key={status} value={status}>
                  {status}
                </option>
              ))}
            </select>
          </div>
        </div>
      ))}
    </div>
  );
}

export function RecruiterDashboard() {
  const { data: jobs, isLoading } = useMyJobs();
  const [expandedJobId, setExpandedJobId] = useState<string | null>(null);

  return (
    <div className="mx-auto max-w-4xl px-6 py-12">
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="font-display text-3xl text-ink">Your job postings</h1>
          <p className="mt-1 text-sm text-muted">Manage postings and review applicants.</p>
        </div>
        <Link to="/post-job">
          <Button>Post a job</Button>
        </Link>
      </div>

      {isLoading ? (
        <div className="flex justify-center py-24">
          <Spinner />
        </div>
      ) : !jobs || jobs.length === 0 ? (
        <EmptyState
          title="No jobs posted yet"
          description="Post your first role to start receiving applications."
        />
      ) : (
        <div className="flex flex-col gap-3">
          {jobs.map((job) => (
            <Card key={job.id} className="p-5">
              <button
                className="flex w-full items-center justify-between text-left"
                onClick={() => setExpandedJobId((current) => (current === job.id ? null : job.id))}
              >
                <div>
                  <p className="font-display text-lg text-ink">{job.title}</p>
                  <p className="mt-0.5 text-sm text-muted">
                    {job.location} · Posted {formatRelativeDate(job.created_at)}
                  </p>
                </div>
                <div className="flex items-center gap-3">
                  <Badge status={job.status}>{job.status}</Badge>
                  <span className="text-muted">{expandedJobId === job.id ? "−" : "+"}</span>
                </div>
              </button>
              {expandedJobId === job.id && <ApplicantsPanel jobId={job.id} />}
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
