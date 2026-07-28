import { useState } from 'react'
import { useJobs } from '@/features/jobs/hooks/use-jobs'
import { JobCard } from '@/features/jobs/components/JobCard'
import { Button } from '@/shared/components/ui/Button'
import { SelectField } from '@/shared/components/ui/primitives'
import { TextField } from '@/shared/components/ui/TextField'
import { EmptyState, Spinner } from '@/shared/components/ui/primitives'
import type { EmploymentType, ExperienceLevel } from '@/shared/types'

const PAGE_SIZE = 9

export function JobsListPage() {
  const [search, setSearch] = useState('')
  const [location, setLocation] = useState('')
  const [employmentType, setEmploymentType] = useState<EmploymentType | ''>('')
  const [experienceLevel, setExperienceLevel] = useState<ExperienceLevel | ''>('')
  const [page, setPage] = useState(1)

  const { data, isLoading, isError, isFetching } = useJobs({
    search: search || undefined,
    location: location || undefined,
    employment_type: employmentType || undefined,
    experience_level: experienceLevel || undefined,
    page,
    page_size: PAGE_SIZE,
  })

  const totalPages = data?.meta.total_pages ?? 0

  return (
    <div className="mx-auto max-w-5xl px-6 py-14">
      <div className="mb-10 border-b border-border pb-8">
        <h1 className="font-display text-[2.5rem] leading-[1.05] tracking-[-0.02em] text-ink">
          Find your next role
        </h1>
        <p className="mt-2 text-[15px] text-muted">
          {data?.meta.total ?? 0} open position{data?.meta.total === 1 ? '' : 's'} right now.
        </p>
      </div>

      <div className="mb-10 grid grid-cols-1 gap-x-6 gap-y-4 rounded-card border border-border bg-white p-5 sm:grid-cols-2 lg:grid-cols-5">
        <div className="lg:col-span-2">
          <TextField
            label="Search"
            placeholder="Job title or keyword"
            value={search}
            onChange={(e) => {
              setPage(1)
              setSearch(e.target.value)
            }}
          />
        </div>
        <TextField
          label="Location"
          placeholder="City or Remote"
          value={location}
          onChange={(e) => {
            setPage(1)
            setLocation(e.target.value)
          }}
        />
        <SelectField
          label="Employment type"
          value={employmentType}
          onChange={(e) => {
            setPage(1)
            setEmploymentType(e.target.value as EmploymentType | '')
          }}
        >
          <option value="">Any type</option>
          <option value="full_time">Full-time</option>
          <option value="part_time">Part-time</option>
          <option value="contract">Contract</option>
          <option value="internship">Internship</option>
        </SelectField>
        <SelectField
          label="Experience"
          value={experienceLevel}
          onChange={(e) => {
            setPage(1)
            setExperienceLevel(e.target.value as ExperienceLevel | '')
          }}
        >
          <option value="">Any level</option>
          <option value="entry">Entry</option>
          <option value="mid">Mid</option>
          <option value="senior">Senior</option>
          <option value="lead">Lead</option>
        </SelectField>
      </div>

      {isLoading ? (
        <div className="flex justify-center py-24">
          <Spinner />
        </div>
      ) : isError ? (
        <EmptyState
          title="Couldn't load jobs"
          description="Something went wrong reaching the server. Try again shortly."
        />
      ) : data && data.jobs.length > 0 ? (
        <>
          <div
            className={`grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 ${isFetching ? 'opacity-60' : ''}`}
          >
            {data.jobs.map((job) => (
              <JobCard key={job.id} job={job} />
            ))}
          </div>

          {totalPages > 1 && (
            <div className="mt-8 flex items-center justify-center gap-3">
              <Button
                variant="secondary"
                size="sm"
                disabled={page <= 1}
                onClick={() => setPage((p) => p - 1)}
              >
                Previous
              </Button>
              <span className="text-sm text-muted">
                Page {page} of {totalPages}
              </span>
              <Button
                variant="secondary"
                size="sm"
                disabled={page >= totalPages}
                onClick={() => setPage((p) => p + 1)}
              >
                Next
              </Button>
            </div>
          )}
        </>
      ) : (
        <EmptyState
          title="No jobs match your filters"
          description="Try clearing a filter or searching a different keyword."
        />
      )}
    </div>
  )
}