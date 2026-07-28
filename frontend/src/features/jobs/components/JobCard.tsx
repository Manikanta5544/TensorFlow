import { Link } from 'react-router-dom'
import type { Job } from '@/shared/types'
import { Card } from '@/shared/components/ui/primitives'
import { formatEmploymentType, formatRelativeDate, formatSalary } from '@/shared/utils/format'

export function JobCard({ job }: { job: Job }) {
  return (
    <Link to={`/jobs/${job.id}`} className="group block">
      <Card className="h-full p-5 transition-all duration-150 group-hover:-translate-y-0.5 group-hover:border-ink/20 group-hover:shadow-md">
        <p className="caption-label text-accent">
          {job.experience_level} · {formatEmploymentType(job.employment_type)}
        </p>

        <h3 className="mt-2 font-display text-lg leading-snug text-ink">{job.title}</h3>
        <p className="mt-0.5 text-sm text-muted">
          {job.company_name} · {job.location}
        </p>

        <p className="mt-3 line-clamp-2 text-sm text-ink/70">{job.description}</p>

        <div className="mt-4 flex items-center justify-between border-t border-border pt-3 text-xs text-muted">
          <span className="font-mono text-ink/80">
            {formatSalary(job.salary_min, job.salary_max)}
          </span>
          <span>{formatRelativeDate(job.created_at)}</span>
        </div>
      </Card>
    </Link>
  )
}
