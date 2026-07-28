"""
Repeatable seed script.

Usage:
    python -m seed.seed
"""

import random

from src.applications.domain.entities import Application, ApplicationStatus
from src.auth.domain.entities import User, UserRole
from src.jobs.domain.entities import EmploymentType, ExperienceLevel, Job
from src.shared.database.session import SessionLocal
from src.shared.security.security import hash_password

COMPANIES = [
    "Acme Corp",
    "Nimbus Systems",
    "Bluepeak Technologies",
    "Orbital Software",
    "Vertex Analytics",
    "Northwind Labs",
    "Cascade Digital",
    "Ironclad Security",
    "Lumen Cloud",
    "Meridian AI",
]

ROLES = [
    ("Senior Backend Engineer", ExperienceLevel.SENIOR, ["Python", "FastAPI", "PostgreSQL"]),
    ("Frontend Engineer", ExperienceLevel.MID, ["React", "TypeScript", "Tailwind CSS"]),
    ("DevOps Engineer", ExperienceLevel.SENIOR, ["Docker", "Kubernetes", "AWS"]),
    ("Full Stack Developer", ExperienceLevel.MID, ["React", "Node.js", "PostgreSQL"]),
    ("Data Engineer", ExperienceLevel.MID, ["Python", "Airflow", "Spark"]),
    ("Engineering Manager", ExperienceLevel.LEAD, ["Leadership", "System Design", "Python"]),
    ("QA Automation Engineer", ExperienceLevel.MID, ["Selenium", "Python", "CI/CD"]),
    ("Product Designer", ExperienceLevel.MID, ["Figma", "User Research", "Prototyping"]),
    ("Junior Software Engineer", ExperienceLevel.ENTRY, ["Python", "Git", "SQL"]),
    ("Machine Learning Engineer", ExperienceLevel.SENIOR, ["Python", "PyTorch", "MLOps"]),
    ("Site Reliability Engineer", ExperienceLevel.SENIOR, ["Linux", "Terraform", "Monitoring"]),
    ("Mobile Engineer (React Native)", ExperienceLevel.MID, ["React Native", "TypeScript", "iOS"]),
    ("Security Engineer", ExperienceLevel.SENIOR, ["AppSec", "Penetration Testing", "Python"]),
    ("Technical Writer", ExperienceLevel.ENTRY, ["Documentation", "Markdown", "API Design"]),
    ("Engineering Intern", ExperienceLevel.ENTRY, ["Python", "Git", "Problem Solving"]),
]

LOCATIONS = ["Hyderabad, India", "Bengaluru, India", "Remote (India)", "Pune, India", "Chennai, India"]

CANDIDATE_NAMES = [
    "Aarav Sharma",
    "Priya Nair",
    "Rohan Gupta",
    "Ananya Iyer",
    "Kabir Khan",
    "Diya Patel",
    "Vihaan Reddy",
    "Ishita Rao",
]

SEED_MARKER_EMAIL = "seed.marker@tensorflow.example.com"


def run() -> None:
    db = SessionLocal()
    try:
        if db.query(User).filter(User.email == SEED_MARKER_EMAIL).first():
            print("Seed data already present — skipping (idempotent).")
            return

        # --- Recruiters (one per company for the first 10 job postings) ---
        recruiters: list[User] = []
        for i, company in enumerate(COMPANIES):
            recruiter = User(
                email=f"recruiter{i+1}@tensorflow.example.com",
                hashed_password=hash_password("DemoPass123!"),
                full_name=f"Recruiter {i+1}",
                role=UserRole.RECRUITER,
                company_name=company,
            )
            db.add(recruiter)
            recruiters.append(recruiter)

        # --- Candidates ---
        candidates: list[User] = []
        for i, name in enumerate(CANDIDATE_NAMES):
            candidate = User(
                email=f"candidate{i+1}@tensorflow.example.com",
                hashed_password=hash_password("DemoPass123!"),
                full_name=name,
                role=UserRole.CANDIDATE,
            )
            db.add(candidate)
            candidates.append(candidate)

        db.add(
            User(
                email=SEED_MARKER_EMAIL,
                hashed_password=hash_password("unused"),
                full_name="Seed Marker",
                role=UserRole.CANDIDATE,
            )
        )
        db.flush()

        # --- Jobs (15) ---
        jobs: list[Job] = []
        for i, (title, level, skills) in enumerate(ROLES):
            recruiter = recruiters[i % len(recruiters)]
            job = Job(
                recruiter_id=recruiter.id,
                title=title,
                company_name=recruiter.company_name,
                location=random.choice(LOCATIONS),
                description=(
                    f"We are hiring a {title} to help us build and scale our platform. "
                    f"You'll work closely with product and engineering on high-impact projects."
                ),
                requirements=f"Experience with: {', '.join(skills)}. {level.value.title()}-level role.",
                employment_type=EmploymentType.FULL_TIME,
                experience_level=level,
                salary_min=random.randint(8, 20) * 100_000,
                salary_max=random.randint(20, 40) * 100_000,
            )
            db.add(job)
            jobs.append(job)
        db.flush()

        # --- Applications (20) ---
        pairs = set()
        applications_created = 0
        attempts = 0
        while applications_created < 20 and attempts < 200:
            attempts += 1
            candidate = random.choice(candidates)
            job = random.choice(jobs)
            key = (candidate.id, job.id)
            if key in pairs:
                continue
            pairs.add(key)
            db.add(
                Application(
                    job_id=job.id,
                    candidate_id=candidate.id,
                    cover_letter=f"I'm excited to apply for the {job.title} role — my background aligns well with what you're looking for.",
                    resume_text=f"{candidate.full_name} — experienced professional with a strong track record relevant to {job.title}.",
                    status=random.choice(list(ApplicationStatus)),
                )
            )
            applications_created += 1

        db.commit()
        print(
            f"Seeded {len(recruiters)} recruiters, {len(candidates)} candidates, "
            f"{len(jobs)} jobs, {applications_created} applications."
        )
        print("Demo login (any seeded account): password is 'DemoPass123!'")
        print("  Recruiter: recruiter1@tensorflow.example.com")
        print("  Candidate: candidate1@tensorflow.example.com")
    finally:
        db.close()


if __name__ == "__main__":
    run()
