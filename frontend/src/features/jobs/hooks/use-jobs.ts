import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import {
  createJob,
  fetchJob,
  fetchJobs,
  fetchMyJobs,
  type CreateJobPayload,
  type JobListParams,
} from '@/features/jobs/api/jobs-api'

export function useJobs(params: JobListParams) {
  return useQuery({
    queryKey: ['jobs', params],
    queryFn: () => fetchJobs(params),
    placeholderData: (previous) => previous,
  })
}

export function useJob(jobId: string | undefined) {
  return useQuery({
    queryKey: ['jobs', jobId],
    queryFn: () => fetchJob(jobId as string),
    enabled: !!jobId,
  })
}

export function useMyJobs() {
  return useQuery({ queryKey: ['jobs', 'mine'], queryFn: fetchMyJobs })
}

export function useCreateJob() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: CreateJobPayload) => createJob(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['jobs'] })
    },
  })
}
