import { describe, expect, it } from "vitest";
import { loginSchema, registerSchema } from "@/features/auth/types/schemas";

describe("loginSchema", () => {
  it("accepts a valid login payload", () => {
    const result = loginSchema.safeParse({ email: "user@example.com", password: "anything" });
    expect(result.success).toBe(true);
  });

  it("rejects an invalid email", () => {
    const result = loginSchema.safeParse({ email: "not-an-email", password: "anything" });
    expect(result.success).toBe(false);
  });
});

describe("registerSchema", () => {
  it("requires company_name when role is recruiter", () => {
    const result = registerSchema.safeParse({
      full_name: "Jane Doe",
      email: "jane@example.com",
      password: "SecurePass1",
      role: "recruiter",
    });
    expect(result.success).toBe(false);
  });

  it("allows a recruiter with a company_name", () => {
    const result = registerSchema.safeParse({
      full_name: "Jane Doe",
      email: "jane@example.com",
      password: "SecurePass1",
      role: "recruiter",
      company_name: "Acme Corp",
    });
    expect(result.success).toBe(true);
  });

  it("does not require company_name for candidates", () => {
    const result = registerSchema.safeParse({
      full_name: "John Candidate",
      email: "john@example.com",
      password: "SecurePass1",
      role: "candidate",
    });
    expect(result.success).toBe(true);
  });

  it("rejects a weak password", () => {
    const result = registerSchema.safeParse({
      full_name: "Jane Doe",
      email: "jane@example.com",
      password: "weak",
      role: "candidate",
    });
    expect(result.success).toBe(false);
  });
});
