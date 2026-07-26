from src.ai.domain.provider import CompletionRequest

JOB_DESCRIPTION_SYSTEM_PROMPT = (
    "You are an expert technical recruiter and copywriter. Write clear, inclusive, "
    "well-structured job descriptions. Use markdown with headings for Responsibilities, "
    "Requirements, and Nice to Have. Avoid biased or exclusionary language. Be concise."
)


def build_job_description_prompt(
    *, role_title: str, experience_level: str, key_skills: list[str], company_context: str = ""
) -> CompletionRequest:
    skills = ", ".join(key_skills)
    user_prompt = (
        f"Write a job description for the role: {role_title}\n"
        f"Experience level: {experience_level}\n"
        f"Key skills required: {skills}\n"
        + (f"Company context: {company_context}\n" if company_context else "")
        + "\nStructure the output with: a 2-sentence role summary, Responsibilities (5-7 bullets), "
        "Requirements (5-7 bullets), and Nice to Have (2-3 bullets)."
    )
    return CompletionRequest(
        system_prompt=JOB_DESCRIPTION_SYSTEM_PROMPT, user_prompt=user_prompt, max_tokens=900
    )
