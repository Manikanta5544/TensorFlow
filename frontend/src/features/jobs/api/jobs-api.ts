import { apiClient } from '@/shared/lib/api-client'
import type { ApiEnvelope, ApiMeta, EmploymentType, ExperienceLevel, Job } from '@/shared/types'

export interface JobListParams {
  search?: string
  location?: string
  employment_type?: EmploymentType
  experience_level?: ExperienceLevel
  page?: number
  page_size?: number
}

export async function fetchJobs(params: JobListParams): Promise<{ jobs: Job[]; meta: ApiMeta }> {
  const res = await apiClient.get<ApiEnvelope<Job[]>>('/jobs', { params })
  return { jobs: res.data.data, meta: res.data.meta }
}

export async function fetchJob(jobId: string): Promise<Job> {
  const res = await apiClient.get<ApiEnvelope<Job>>(`/jobs/${jobId}`)
  return res.data.data
}

export async function fetchMyJobs(): Promise<Job[]> {
  const res = await apiClient.get<ApiEnvelope<Job[]>>('/jobs/mine/list')
  return res.data.data
}

export interface CreateJobPayload {
  title: string
  company_name: string
  location: string
  description: string
  requirements: string
  employment_type: EmploymentType
  experience_level: ExperienceLevel
  salary_min?: number
  salary_max?: number
}

export async function createJob(payload: CreateJobPayload): Promise<Job> {
  const res = await apiClient.post<ApiEnvelope<Job>>('/jobs', payload)
  return res.data.data
}
