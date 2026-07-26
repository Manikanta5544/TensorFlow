import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { useApplyToJob } from "@/features/applications/hooks/use-applications";
import { Button } from "@/shared/components/ui/Button";
import { TextAreaField } from "@/shared/components/ui/TextField";
import { getApiErrorMessage } from "@/shared/lib/api-client";

const applySchema = z.object({
  cover_letter: z.string().max(5000).optional().default(""),
  resume_text: z.string().min(20, "Add a bit more detail — at least 20 characters."),
});
type ApplyFormValues = z.infer<typeof applySchema>;

export function ApplyModal({
  jobTitle,
  onClose,
  jobId,
}: {
  jobTitle: string;
  jobId: string;
  onClose: () => void;
}) {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<ApplyFormValues>({ resolver: zodResolver(applySchema) });

  const mutation = useApplyToJob();

  if (mutation.isSuccess) {
    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-ink/40 px-4">
        <div className="w-full max-w-md rounded-card bg-white p-6 text-center shadow-popover">
          <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-success-soft text-success">
            ✓
          </div>
          <h2 className="mt-4 font-display text-xl text-ink">Application sent</h2>
          <p className="mt-1 text-sm text-muted">
            Your application for {jobTitle} is in. Track it from your dashboard.
          </p>
          <Button className="mt-6 w-full" onClick={onClose}>
            Done
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-ink/40 px-4"
      role="dialog"
      aria-modal="true"
    >
      <div className="w-full max-w-lg rounded-card bg-white p-6 shadow-popover">
        <div className="flex items-start justify-between">
          <div>
            <h2 className="font-display text-xl text-ink">Apply to {jobTitle}</h2>
            <p className="mt-1 text-sm text-muted">
              Keep it focused — a few honest sentences beat a form letter.
            </p>
          </div>
          <button onClick={onClose} aria-label="Close" className="text-muted hover:text-ink">
            ✕
          </button>
        </div>

        <form
          onSubmit={handleSubmit((values) => mutation.mutate({ jobId, ...values }))}
          className="mt-5 flex flex-col gap-4"
        >
          <TextAreaField
            label="Resume summary"
            rows={5}
            placeholder="Paste a summary of your experience, skills, and relevant background."
            error={errors.resume_text?.message}
            {...register("resume_text")}
          />
          <TextAreaField
            label="Cover letter (optional)"
            rows={4}
            placeholder="Why this role, why you?"
            error={errors.cover_letter?.message}
            {...register("cover_letter")}
          />

          {mutation.isError && (
            <p className="rounded-lg bg-danger-soft px-3.5 py-2.5 text-sm text-danger">
              {getApiErrorMessage(mutation.error, "Unable to submit your application.")}
            </p>
          )}

          <div className="mt-1 flex justify-end gap-3">
            <Button type="button" variant="secondary" onClick={onClose}>
              Cancel
            </Button>
            <Button type="submit" isLoading={mutation.isPending}>
              Submit application
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}
