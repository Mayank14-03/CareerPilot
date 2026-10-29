
import re


SKILL_ALIASES = {
    "Python": [r"\bpython\b"],
    "AWS": [r"\baws\b", r"\bamazon web services\b", r"\ba\s+ws\b"],
    "Boto3": [r"\bboto3\b"],
    "Linux": [r"\blinux\b"],
    "Git": [r"\bgit\b"],
    "GitHub": [r"\bgithub\b"],
    "SQL": [r"\bsql\b"],
    "Django": [r"\bdjango\b"],
    "REST API": [r"\brest\s+apis?\b"],
    "PostgreSQL": [r"\bpostgres(?:ql)?\b"],
    "MySQL": [r"\bmysql\b"],
    "Terraform": [r"\bterraform\b"],
    "Docker": [r"\bdocker\b"],
    "Kubernetes": [r"\bkubernetes\b"],
    "Bash": [r"\bbash\b", r"\bshell scripting\b"],
    "PowerShell": [r"\bpowershell\b"],
    "FastAPI": [r"\bfastapi\b"],
    "Flask": [r"\bflask\b"],
    "CloudWatch": [r"\bcloudwatch\b"],
    "EC2": [r"\bec2\b"],
    "S3": [r"\bs3\b"],
    "IAM": [r"\biam\b"],
    "VPC": [r"\bvpc\b"],
}


def extract_skills(text: str) -> list[str]:
    """Extract recognized skills from resume text."""

    if not text or not text.strip():
        return []

    found_skills = []

    for skill, patterns in SKILL_ALIASES.items():
        if any(
            re.search(pattern, text, re.IGNORECASE)
            for pattern in patterns
        ):
            found_skills.append(skill)

    return found_skills
