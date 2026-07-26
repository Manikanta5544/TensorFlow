import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import { Link, useNavigate } from "react-router-dom";
import { loginRequest } from "@/features/auth/api/auth-api";
import { useAuth } from "@/features/auth/auth-context";
import { loginSchema, type LoginFormValues } from "@/features/auth/types/schemas";
import { Button } from "@/shared/components/ui/Button";
import { TextField } from "@/shared/components/ui/TextField";
import { getApiErrorMessage } from "@/shared/lib/api-client";

export function LoginPage() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormValues>({ resolver: zodResolver(loginSchema) });

  const mutation = useMutation({
    mutationFn: loginRequest,
    onSuccess: (data) => {
      login(data.access_token, data.user);
      navigate(data.user.role === "recruiter" ? "/dashboard" : "/jobs");
    },
  });

  return (
    <div className="mx-auto flex min-h-[calc(100vh-64px)] max-w-md flex-col justify-center px-6 py-16">
      <h1 className="font-display text-3xl text-ink">Welcome back</h1>
      <p className="mt-2 text-sm text-muted">Sign in to continue to TalentFlow AI.</p>

      <form onSubmit={handleSubmit((values) => mutation.mutate(values))} className="mt-8 flex flex-col gap-4">
        <TextField
          label="Email"
          type="email"
          autoComplete="email"
          error={errors.email?.message}
          {...register("email")}
        />
        <TextField
          label="Password"
          type="password"
          autoComplete="current-password"
          error={errors.password?.message}
          {...register("password")}
        />

        {mutation.isError && (
          <p className="rounded-lg bg-danger-soft px-3.5 py-2.5 text-sm text-danger">
            {getApiErrorMessage(mutation.error, "Unable to sign in.")}
          </p>
        )}

        <Button type="submit" isLoading={mutation.isPending} className="mt-2 w-full">
          Sign in
        </Button>
      </form>

      <p className="mt-6 text-center text-sm text-muted">
        New to TalentFlow AI?{" "}
        <Link to="/register" className="font-medium text-accent hover:underline">
          Create an account
        </Link>
      </p>

      <div className="mt-10 rounded-lg border border-border bg-white p-4 text-xs text-muted">
        <p className="font-medium text-ink">Demo accounts (after seeding)</p>
        <p className="mt-1">Recruiter: recruiter1@talentflow.example.com</p>
        <p>Candidate: candidate1@talentflow.example.com</p>
        <p>Password: DemoPass123!</p>
      </div>
    </div>
  );
}
