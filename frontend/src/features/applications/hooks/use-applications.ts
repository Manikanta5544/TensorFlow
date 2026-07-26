import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { apiClient } from "@/shared/lib/api-client";
import type { ApiEnvelope, ApplicationStatus, JobApplication } from "@/shared/types";

interface ApplyPayload {
  jobId: string;
  cover_letter: string;
  resume_text: string;
}

async function applyToJob({ jobId, ...payload }: ApplyPayload): Promise<JobApplication> {
  const res = await apiClient.post<ApiEnvelope<JobApplication>>(`/jobs/${jobId}/applications`, payload);
  return res.data.data;
}

export function useApplyToJob() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: applyToJob,
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({ queryKey: ["applications", "mine"] });
      queryClient.invalidateQueries({ queryKey: ["applications", "job", variables.jobId] });
    },
  });
}

async function fetchMyApplications(): Promise<JobApplication[]> {
  const res = await apiClient.get<ApiEnvelope<JobApplication[]>>("/applications/mine");
  return res.data.data;
}

export function useMyApplications() {
  return useQuery({ queryKey: ["applications", "mine"], queryFn: fetchMyApplications });
}

async function fetchApplicationsForJob(jobId: string): Promise<JobApplication[]> {
  const res = await apiClient.get<ApiEnvelope<JobApplication[]>>(`/jobs/${jobId}/applications`);
  return res.data.data;
}

export function useApplicationsForJob(jobId: string | undefined) {
  return useQuery({
    queryKey: ["applications", "job", jobId],
    queryFn: () => fetchApplicationsForJob(jobId as string),
    enabled: !!jobId,
  });
}

async function updateApplicationStatus(
  applicationId: string,
  status: ApplicationStatus,
): Promise<JobApplication> {
  const res = await apiClient.patch<ApiEnvelope<JobApplication>>(`/applications/${applicationId}/status`, {
    status,
  });
  return res.data.data;
}

export function useUpdateApplicationStatus(jobId: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ applicationId, status }: { applicationId: string; status: ApplicationStatus }) =>
      updateApplicationStatus(applicationId, status),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["applications", "job", jobId] });
    },
  });
}
