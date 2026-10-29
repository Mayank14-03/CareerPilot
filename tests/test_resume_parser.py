
from app.services.resume_parser import extract_skills


def test_extract_skills():
    resume_text = """
    Python, AWS, Boto3, Linux, Git, PostgreSQL,
    Django, Terraform, Docker and FastAPI.
    """

    result = extract_skills(resume_text)

    assert "Python" in result
    assert "AWS" in result
    assert "Boto3" in result
    assert "Linux" in result
    assert "PostgreSQL" in result
    assert "Django" in result
    assert "Terraform" in result


def test_extract_skills_empty_text():
    assert extract_skills("") == []
