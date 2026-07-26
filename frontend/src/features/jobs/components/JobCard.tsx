import { Link } from "react-router-dom";
import type { Job } from "@/shared/types";
import { Badge, Card } from "@/shared/components/ui/primitives";
import { formatEmploymentType, formatRelativeDate, formatSalary } from "@/shared/utils/format";

export function JobCard({ job }: { job: Job }) {
  return (
    <Link to={`/jobs/${job.id}`}>
      <Card className="p-5 transition-shadow hover:shadow-popover">
        <div className="flex items-start justify-between gap-3">
          <div>
            <h3 className="font-display text-lg text-ink">{job.title}</h3>
            <p className="mt-0.5 text-sm text-muted">
              {job.company_name} · {job.location}
            </p>
          </div>
          <Badge status={job.experience_level}>{job.experience_level}</Badge>
        </div>

        <p className="mt-3 line-clamp-2 text-sm text-ink/80">{job.description}</p>

        <div className="mt-4 flex flex-wrap items-center gap-x-4 gap-y-1 text-xs text-muted">
          <span className="font-mono">{formatSalary(job.salary_min, job.salary_max)}</span>
          <span>{formatEmploymentType(job.employment_type)}</span>
          <span className="ml-auto">{formatRelativeDate(job.created_at)}</span>
        </div>
      </Card>
    </Link>
  );
}
