
SKILL_RECOMMENDATIONS = {
    "django": {
        "priority": "High",
        "recommendation": (
            "Learn Django fundamentals, models, views, URL routing, "
            "and CRUD operations. Build a small job-tracker application."
        ),
    },
    "rest api": {
        "priority": "High",
        "recommendation": (
            "Learn REST principles, HTTP methods, status codes, "
            "request validation, and API testing. Build and test a CRUD API."
        ),
    },
    "python": {
        "priority": "High",
        "recommendation": (
            "Practice Python functions, data structures, exception handling, "
            "file handling, and object-oriented programming."
        ),
    },
    "sql": {
        "priority": "Medium",
        "recommendation": (
            "Practice SQL queries, joins, filtering, aggregation, "
            "and database CRUD operations."
        ),
    },
    "git": {
        "priority": "Medium",
        "recommendation": (
            "Practice Git commits, branches, merging, and pushing projects "
            "to GitHub."
        ),
    },
}


def generate_recommendations(missing_skills):
    """Generate learning recommendations for missing skills."""

    recommendations = []

    for skill in missing_skills:
        normalized_skill = skill.strip().casefold()

        recommendation = SKILL_RECOMMENDATIONS.get(
            normalized_skill
        )

        if recommendation:
            recommendations.append({
                "skill": skill,
                "priority": recommendation["priority"],
                "recommendation": recommendation["recommendation"],
            })
        else:
            recommendations.append({
                "skill": skill,
                "priority": "Medium",
                "recommendation": (
                    f"Learn the fundamentals of {skill} and build "
                    "a small practical project to demonstrate your skills."
                ),
            })

    return recommendations
