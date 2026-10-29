
from app.services.skill_analyzer import analyze_skills


def test_analyze_skills():
    result = analyze_skills(
        candidate_skills=["Python", "SQL", "Git"],
        required_skills=[
            "Python",
            "SQL",
            "Django",
            "REST API",
            "Git",
        ],
    )

    assert result["matched_skills"] == ["git", "python", "sql"]
    assert result["missing_skills"] == ["django", "rest api"]
    assert result["match_percentage"] == 60.0


def test_postgresql_matches_sql_requirement():
    result = analyze_skills(
        candidate_skills=["PostgreSQL"],
        required_skills=["SQL"],
    )

    assert result["matched_skills"] == ["sql"]
    assert result["missing_skills"] == []
    assert result["match_percentage"] == 100.0


def test_mysql_matches_sql_requirement():
    result = analyze_skills(
        candidate_skills=["MySQL"],
        required_skills=["SQL"],
    )

    assert result["matched_skills"] == ["sql"]
    assert result["missing_skills"] == []
    assert result["match_percentage"] == 100.0


def test_postgresql_does_not_match_mysql_requirement():
    result = analyze_skills(
        candidate_skills=["PostgreSQL"],
        required_skills=["MySQL"],
    )

    assert result["matched_skills"] == []
    assert result["missing_skills"] == ["mysql"]
    assert result["match_percentage"] == 0.0


def test_mysql_does_not_match_postgresql_requirement():
    result = analyze_skills(
        candidate_skills=["MySQL"],
        required_skills=["PostgreSQL"],
    )

    assert result["matched_skills"] == []
    assert result["missing_skills"] == ["postgresql"]
    assert result["match_percentage"] == 0.0
