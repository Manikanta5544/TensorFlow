import { zodResolver } from "@hookform/resolvers/zod";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";
import { z } from "zod";
import { useGenerateJobDescription } from "@/features/ai/api/ai-api";
import { useCreateJob } from "@/features/jobs/hooks/use-jobs";
import { Button } from "@/shared/components/ui/Button";
import { SelectField } from "@/shared/components/ui/primitives";
import { TextAreaField, TextField } from "@/shared/components/ui/TextField";
import { getApiErrorMessage } from "@/shared/lib/api-client";

const postJobSchema = z
  .object({
    title: z.string().min(3, "Title is too short"),
    company_name: z.string().min(1, "Company name is required"),
    location: z.string().min(1, "Location is required"),
    description: z.string().min(20, "Description should be at least 20 characters"),
    requirements: z.string().optional().default(""),
    employment_type: z.enum(["full_time", "part_time", "contract", "internship"]),
    experience_level: z.enum(["entry", "mid", "senior", "lead"]),
    salary_min: z.coerce.number().int().nonnegative().optional().or(z.literal("")),
    salary_max: z.coerce.number().int().nonnegative().optional().or(z.literal("")),
  })
  .refine(
    (data) => !data.salary_min || !data.salary_max || Number(data.salary_min) <= Number(data.salary_max),
    { message: "Minimum salary can't exceed the maximum", path: ["salary_max"] },
  );
type PostJobFormValues = z.infer<typeof postJobSchema>;

export function PostJobPage() {
  const navigate = useNavigate();
  const [skillsInput, setSkillsInput] = useState("");

  const {
    register,
    handleSubmit,
    watch,
    setValue,
    formState: { errors },
  } = useForm<PostJobFormValues>({
    resolver: zodResolver(postJobSchema),
    defaultValues: { employment_type: "full_time", experience_level: "mid" },
  });

  const createJobMutation = useCreateJob();
  const generateMutation = useGenerateJobDescription();

  async function handleGenerate() {
    const title = watch("title");
    const level = watch("experience_level");
    if (!title) return;
    const skills = skillsInput
      .split(",")
      .map((s) => s.trim())
      .filter(Boolean);
    const text = await generateMutation.mutateAsync({
      role_title: title,
      experience_level: level,
      key_skills: skills.length ? skills : [title],
    });
    setValue("description", text, { shouldValidate: true });
  }

  function onSubmit(values: PostJobFormValues) {
    createJobMutation.mutate(
      {
        ...values,
        salary_min: values.salary_min === "" ? undefined : Number(values.salary_min),
        salary_max: values.salary_max === "" ? undefined : Number(values.salary_max),
      },
      { onSuccess: (job) => navigate(`/jobs/${job.id}`) },
    );
  }

  return (
    <div className="mx-auto max-w-2xl px-6 py-12">
      <h1 className="font-display text-3xl text-ink">Post a new job</h1>
      <p className="mt-1 text-sm text-muted">Fill in the basics — or let AI draft the description for you.</p>

      <form onSubmit={handleSubmit(onSubmit)} className="mt-8 flex flex-col gap-4">
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <TextField label="Job title" error={errors.title?.message} {...register("title")} />
          <TextField
            label="Company name"
            error={errors.company_name?.message}
            {...register("company_name")}
          />
        </div>

        <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
          <TextField label="Location" error={errors.location?.message} {...register("location")} />
          <SelectField label="Employment type" {...register("employment_type")}>
            <option value="full_time">Full-time</option>
            <option value="part_time">Part-time</option>
            <option value="contract">Contract</option>
            <option value="internship">Internship</option>
          </SelectField>
          <SelectField label="Experience level" {...register("experience_level")}>
            <option value="entry">Entry</option>
            <option value="mid">Mid</option>
            <option value="senior">Senior</option>
            <option value="lead">Lead</option>
          </SelectField>
        </div>

        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <TextField
            label="Minimum salary (₹/yr)"
            type="number"
            error={errors.salary_min?.message}
            {...register("salary_min")}
          />
          <TextField
            label="Maximum salary (₹/yr)"
            type="number"
            error={errors.salary_max?.message}
            {...register("salary_max")}
          />
        </div>

        <div className="rounded-card border border-accent/30 bg-accent-soft/40 p-4">
          <p className="text-sm font-medium text-ink">AI description assist</p>
          <p className="mt-0.5 text-xs text-muted">
            Enter a title above, add a few key skills (comma-separated), then generate a draft.
          </p>
          <div className="mt-3 flex flex-col gap-2 sm:flex-row">
            <input
              value={skillsInput}
              onChange={(e) => setSkillsInput(e.target.value)}
              placeholder="e.g. Python, FastAPI, PostgreSQL"
              className="flex-1 rounded-lg border border-border bg-white px-3.5 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-accent/40 focus:border-accent"
            />
            <Button
              type="button"
              variant="secondary"
              isLoading={generateMutation.isPending}
              disabled={!watch("title")}
              onClick={handleGenerate}
            >
              Generate description
            </Button>
          </div>
          {generateMutation.isError && (
            <p className="mt-2 text-xs text-danger">{getApiErrorMessage(generateMutation.error)}</p>
          )}
        </div>

        <TextAreaField
          label="Description"
          rows={8}
          error={errors.description?.message}
          {...register("description")}
        />
        <TextAreaField
          label="Requirements (optional)"
          rows={4}
          error={errors.requirements?.message}
          {...register("requirements")}
        />

        {createJobMutation.isError && (
          <p className="rounded-lg bg-danger-soft px-3.5 py-2.5 text-sm text-danger">
            {getApiErrorMessage(createJobMutation.error, "Unable to post this job.")}
          </p>
        )}

        <Button type="submit" isLoading={createJobMutation.isPending} className="mt-2 self-start">
          Publish job
        </Button>
      </form>
    </div>
  );
}
