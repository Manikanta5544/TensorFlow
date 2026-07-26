import axios from "axios";

const baseURL = import.meta.env.VITE_API_URL ? `${import.meta.env.VITE_API_URL}/api/v1` : "/api/v1";

export const apiClient = axios.create({ baseURL });

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("talentflow_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export interface ApiErrorBody {
  success: false;
  error: {
    code: string;
    message: string;
    details?: unknown;
  };
}

export function getApiErrorMessage(error: unknown, fallback = "Something went wrong."): string {
  if (axios.isAxiosError<ApiErrorBody>(error) && error.response?.data?.error?.message) {
    return error.response.data.error.message;
  }
  return fallback;
}
