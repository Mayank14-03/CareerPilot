
from app.services.recommendation_engine import generate_recommendations


def test_generate_recommendations():
    result = generate_recommendations(
        ["django", "rest api"]
    )

    assert len(result) == 2
    assert result[0]["skill"] == "django"
    assert result[0]["priority"] == "High"
    assert "Django" in result[0]["recommendation"]

    assert result[1]["skill"] == "rest api"
    assert result[1]["priority"] == "High"


def test_unknown_skill_gets_generic_recommendation():
    result = generate_recommendations(["Kubernetes"])

    assert len(result) == 1
    assert result[0]["skill"] == "Kubernetes"
    assert result[0]["priority"] == "Medium"
    assert "Kubernetes" in result[0]["recommendation"]


def test_empty_missing_skills():
    assert generate_recommendations([]) == []
