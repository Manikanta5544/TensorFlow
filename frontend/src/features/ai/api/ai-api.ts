import { useMutation } from "@tanstack/react-query";
import { apiClient } from "@/shared/lib/api-client";
import type { ApiEnvelope } from "@/shared/types";

interface GenerateJobDescriptionPayload {
  role_title: string;
  experience_level: string;
  key_skills: string[];
}

async function generateJobDescription(payload: GenerateJobDescriptionPayload): Promise<string> {
  const res = await apiClient.post<ApiEnvelope<{ generated_description: string }>>(
    "/ai/job-description",
    payload,
  );
  return res.data.data.generated_description;
}

export function useGenerateJobDescription() {
  return useMutation({ mutationFn: generateJobDescription });
}
