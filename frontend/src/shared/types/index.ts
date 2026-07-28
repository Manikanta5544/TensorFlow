export type UserRole = 'recruiter' | 'candidate'

export interface User {
  id: string
  email: string
  full_name: string
  role: UserRole
  company_name: string | null
}

export type EmploymentType = 'full_time' | 'part_time' | 'contract' | 'internship'
export type ExperienceLevel = 'entry' | 'mid' | 'senior' | 'lead'
export type JobStatus = 'open' | 'closed'

export interface Job {
  id: string
  recruiter_id: string
  title: string
  company_name: string
  location: string
  description: string
  requirements: string
  employment_type: EmploymentType
  experience_level: ExperienceLevel
  salary_min: number | null
  salary_max: number | null
  status: JobStatus
  created_at: string
  updated_at: string
}

export type ApplicationStatus = 'submitted' | 'reviewed' | 'rejected' | 'accepted'

export interface JobApplication {
  id: string
  job_id: string
  candidate_id: string
  cover_letter: string
  resume_text: string
  status: ApplicationStatus
  created_at: string
  updated_at: string
}

export interface ApiMeta {
  page?: number
  page_size?: number
  total?: number
  total_pages?: number
}

export interface ApiEnvelope<T> {
  success: true
  data: T
  meta: ApiMeta
}
