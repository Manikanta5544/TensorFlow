import { useState } from "react";
import { useParams } from "react-router-dom";
import { useAuth } from "@/features/auth/auth-context";
import { useJob } from "@/features/jobs/hooks/use-jobs";
import { ApplyModal } from "@/features/applications/components/ApplyModal";
import { Badge } from "@/shared/components/ui/primitives";
import { Button } from "@/shared/components/ui/Button";
import { Spinner } from "@/shared/components/ui/primitives";
import { formatEmploymentType, formatRelativeDate, formatSalary } from "@/shared/utils/format";

export function JobDetailPage() {
  const { jobId } = useParams<{ jobId: string }>();
  const { user } = useAuth();
  const { data: job, isLoading, isError } = useJob(jobId);
  const [showApply, setShowApply] = useState(false);

  if (isLoading) {
    return (
      <div className="flex justify-center py-24">
        <Spinner />
      </div>
    );
  }

  if (isError || !job) {
    return (
      <div className="mx-auto max-w-2xl px-6 py-24 text-center">
        <p className="font-display text-xl text-ink">Job not found</p>
        <p className="mt-1 text-sm text-muted">It may have been closed or removed.</p>
      </div>
    );
  }

  const canApply = user?.role === "candidate";

  return (
    <div className="mx-auto max-w-3xl px-6 py-12">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h1 className="font-display text-3xl text-ink">{job.title}</h1>
          <p className="mt-1 text-sm text-muted">
            {job.company_name} · {job.location}
          </p>
        </div>
        <Badge status={job.status}>{job.status}</Badge>
      </div>

      <div className="mt-5 flex flex-wrap items-center gap-x-5 gap-y-2 text-sm text-muted">
        <span className="font-mono text-ink">{formatSalary(job.salary_min, job.salary_max)}</span>
        <span>{formatEmploymentType(job.employment_type)}</span>
        <span className="capitalize">{job.experience_level} level</span>
        <span>Posted {formatRelativeDate(job.created_at)}</span>
      </div>

      {canApply && (
        <Button className="mt-6" onClick={() => setShowApply(true)}>
          Apply now
        </Button>
      )}
      {!user && (
        <p className="mt-6 text-sm text-muted">
          <a href="/login" className="font-medium text-accent hover:underline">
            Sign in
          </a>{" "}
          as a candidate to apply.
        </p>
      )}

      <section className="mt-10">
        <h2 className="font-display text-lg text-ink">About the role</h2>
        <p className="mt-2 whitespace-pre-wrap text-sm leading-relaxed text-ink/80">{job.description}</p>
      </section>

      {job.requirements && (
        <section className="mt-8">
          <h2 className="font-display text-lg text-ink">Requirements</h2>
          <p className="mt-2 whitespace-pre-wrap text-sm leading-relaxed text-ink/80">{job.requirements}</p>
        </section>
      )}

      {showApply && <ApplyModal jobId={job.id} jobTitle={job.title} onClose={() => setShowApply(false)} />}
    </div>
  );
}
