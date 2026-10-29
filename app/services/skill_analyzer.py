
SKILL_ALIASES = {
    "sql": {"sql"},
    "postgresql": {"postgresql", "postgres"},
    "mysql": {"mysql"},
    "rest api": {"rest api", "rest apis"},
}


def normalize_skill(skill: str) -> str:
    """Normalize skill names without merging distinct technologies."""

    normalized = " ".join(skill.strip().casefold().split())

    for canonical_skill, aliases in SKILL_ALIASES.items():
        if normalized == canonical_skill or normalized in aliases:
            return canonical_skill

    return normalized


def analyze_skills(candidate_skills, required_skills):
    """Compare candidate skills with job requirements."""

    candidate_set = {
        normalize_skill(skill)
        for skill in candidate_skills
        if skill and skill.strip()
    }

    required_set = {
        normalize_skill(skill)
        for skill in required_skills
        if skill and skill.strip()
    }

    # Keep track of database-specific skills before inferring SQL.
    database_skills = candidate_set & {"mysql", "postgresql"}

    # MySQL and PostgreSQL indicate general SQL knowledge.
    if database_skills:
        candidate_set.add("sql")

    matched_skills = sorted(candidate_set & required_set)

    # Inferred SQL must not count as a match when the job requires
    # a specific database technology instead of general SQL.
    if database_skills and "sql" not in required_set:
        matched_skills = [
            skill for skill in matched_skills
            if skill != "sql"
        ]

    missing_skills = sorted(required_set - set(matched_skills))

    if not required_set:
        match_percentage = 0.0
    else:
        match_percentage = round(
            len(matched_skills) / len(required_set) * 100,
            2,
        )

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_percentage": match_percentage,
    }
