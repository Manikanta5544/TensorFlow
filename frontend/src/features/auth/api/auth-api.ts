import { apiClient } from "@/shared/lib/api-client";
import type { ApiEnvelope, User } from "@/shared/types";
import type { LoginFormValues, RegisterFormValues } from "@/features/auth/types/schemas";

interface AuthResponse {
  user: User;
  access_token: string;
  token_type: string;
}

export async function loginRequest(payload: LoginFormValues): Promise<AuthResponse> {
  const res = await apiClient.post<ApiEnvelope<AuthResponse>>("/auth/login", payload);
  return res.data.data;
}

export async function registerRequest(payload: RegisterFormValues): Promise<AuthResponse> {
  const res = await apiClient.post<ApiEnvelope<AuthResponse>>("/auth/register", payload);
  return res.data.data;
}
