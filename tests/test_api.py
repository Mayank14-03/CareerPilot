
from fastapi.testclient import TestClient

from app.main import app
from app.database import get_db
from unittest.mock import MagicMock


client = TestClient(app)


def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to CareerPilot!"


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_analyze_skills_endpoint():
    response = client.post(
        "/analyze-skills",
        json={
            "candidate_skills": ["Python", "SQL", "Git"],
            "required_skills": [
                "Python",
                "SQL",
                "Django",
                "REST API",
                "Git",
            ],
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["match_percentage"] == 60.0
    assert data["missing_skills"] == ["django", "rest api"]


def test_analyze_saved_job():
    mock_db = MagicMock()

    mock_job = MagicMock()
    mock_job.id = 1
    mock_job.company_name = "ASW Technologies"
    mock_job.job_title = "Junior Python Developer"
    mock_job.required_skills = [
        "Python",
        "SQL",
        "Django",
        "REST API",
        "Git",
    ]

    mock_db.get.return_value = mock_job

    app.dependency_overrides[get_db] = lambda: mock_db

    try:
        response = client.post(
            "/jobs/1/analyze",
            json={"candidate_skills": ["Python", "SQL", "Git"]},
        )

        assert response.status_code == 200

        data = response.json()
        assert data["job_id"] == 1
        assert data["match_percentage"] == 60.0
        assert data["missing_skills"] == ["django", "rest api"]

    finally:
        app.dependency_overrides.clear()


def test_analyze_nonexistent_job():
    mock_db = MagicMock()
    mock_db.get.return_value = None

    app.dependency_overrides[get_db] = lambda: mock_db

    try:
        response = client.post(
            "/jobs/999999/analyze",
            json={"candidate_skills": ["Python", "SQL"]},
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Job not found."

    finally:
        app.dependency_overrides.clear()


def test_analyze_resume_returns_recommendations():
    from io import BytesIO
    from pypdf import PdfWriter

    # Create a small in-memory PDF for testing
    pdf_buffer = BytesIO()
    pdf_writer = PdfWriter()
    pdf_writer.add_blank_page(width=300, height=300)
    pdf_writer.write(pdf_buffer)
    pdf_content = pdf_buffer.getvalue()

    # Mock the job database response
    mock_db = MagicMock()

    mock_job = MagicMock()
    mock_job.id = 1
    mock_job.company_name = "ASW Technologies"
    mock_job.job_title = "Junior Python Developer"
    mock_job.required_skills = [
        "Python",
        "Django",
        "REST API",
    ]

    mock_db.get.return_value = mock_job

    app.dependency_overrides[get_db] = lambda: mock_db

    try:
        # Mock resume text extraction to provide readable text
        from unittest.mock import patch

        with patch(
            "app.main.PdfReader"
        ) as mock_pdf_reader:
            mock_page = MagicMock()
            mock_page.extract_text.return_value = (
                "Python developer with Python and Git skills."
            )

            mock_reader = MagicMock()
            mock_reader.is_encrypted = False
            mock_reader.pages = [mock_page]

            mock_pdf_reader.return_value = mock_reader

            response = client.post(
                "/jobs/1/analyze-resume",
                files={
                    "file": (
                        "test_resume.pdf",
                        pdf_content,
                        "application/pdf",
                    )
                },
            )

        assert response.status_code == 200

        data = response.json()

        assert data["job_id"] == 1
        assert "recommendations" in data

        recommended_skills = [
            item["skill"]
            for item in data["recommendations"]
        ]

        assert "django" in recommended_skills
        assert "rest api" in recommended_skills

        for item in data["recommendations"]:
            assert item["priority"] == "High"
            assert item["recommendation"]

    finally:
        app.dependency_overrides.clear()

def test_create_application():
    from unittest.mock import MagicMock

    mock_db = MagicMock()

    def refresh_application(application):
        application.id = 1

    mock_db.refresh.side_effect = refresh_application

    app.dependency_overrides[get_db] = lambda: mock_db

    try:
        response = client.post(
            "/applications",
            json={
                "company_name": "ASW Technologies",
                "job_title": "Junior Python Developer",
                "application_date": "2026-10-30",
                "status": "Applied",
                "notes": "Applied through HR email.",
            },
        )

        assert response.status_code == 201

        data = response.json()

        assert data["id"] == 1
        assert data["company_name"] == "ASW Technologies"
        assert data["job_title"] == "Junior Python Developer"
        assert data["status"] == "Applied"
        assert data["notes"] == "Applied through HR email."

        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()

    finally:
        app.dependency_overrides.clear()

def test_list_applications():
    from datetime import date
    from types import SimpleNamespace
    from unittest.mock import MagicMock

    mock_db = MagicMock()

    mock_application = SimpleNamespace(
        id=1,
        company_name="ASW Technologies",
        job_title="Junior Python Developer",
        application_date=date(2026, 10, 30),
        status="Applied",
        notes="Applied through HR email.",
    )

    mock_db.query.return_value.order_by.return_value.all.return_value = [
        mock_application
    ]

    app.dependency_overrides[get_db] = lambda: mock_db

    try:
        response = client.get("/applications")

        assert response.status_code == 200

        data = response.json()

        assert len(data) == 1
        assert data[0]["id"] == 1
        assert data[0]["company_name"] == "ASW Technologies"
        assert data[0]["status"] == "Applied"

    finally:
        app.dependency_overrides.clear()

def test_get_application_by_id():
    from datetime import date
    from types import SimpleNamespace
    from unittest.mock import MagicMock

    mock_db = MagicMock()

    mock_application = SimpleNamespace(
        id=1,
        company_name="ASW Technologies",
        job_title="Junior Python Developer",
        application_date=date(2026, 10, 30),
        status="Applied",
        notes="Applied through HR email.",
    )

    mock_db.get.return_value = mock_application

    app.dependency_overrides[get_db] = lambda: mock_db

    try:
        response = client.get("/applications/1")

        assert response.status_code == 200

        data = response.json()

        assert data["id"] == 1
        assert data["company_name"] == "ASW Technologies"
        assert data["job_title"] == "Junior Python Developer"
        assert data["status"] == "Applied"

        mock_db.get.assert_called_once()

    finally:
        app.dependency_overrides.clear()

def test_get_nonexistent_application():
    from unittest.mock import MagicMock

    mock_db = MagicMock()
    mock_db.get.return_value = None

    app.dependency_overrides[get_db] = lambda: mock_db

    try:
        response = client.get("/applications/999999")

        assert response.status_code == 404
        assert response.json()["detail"] == "Job application not found."

    finally:
        app.dependency_overrides.clear()

def test_update_application():
    from datetime import date
    from types import SimpleNamespace
    from unittest.mock import MagicMock

    mock_db = MagicMock()

    mock_application = SimpleNamespace(
        id=1,
        company_name="ASW Technologies",
        job_title="Junior Python Developer",
        application_date=date(2026, 10, 30),
        status="Applied",
        notes="Applied through HR email.",
    )

    mock_db.get.return_value = mock_application

    app.dependency_overrides[get_db] = lambda: mock_db

    try:
        response = client.put(
            "/applications/1",
            json={
                "company_name": "ASW Technologies",
                "job_title": "Junior Python Developer",
                "application_date": "2026-10-30",
                "status": "Interview",
                "notes": "Interview scheduled.",
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["id"] == 1
        assert data["status"] == "Interview"
        assert data["notes"] == "Interview scheduled."

        mock_db.commit.assert_called_once()

    finally:
        app.dependency_overrides.clear()

def test_delete_application():
    from datetime import date
    from types import SimpleNamespace
    from unittest.mock import MagicMock

    mock_db = MagicMock()

    mock_application = SimpleNamespace(
        id=1,
        company_name="ASW Technologies",
        job_title="Junior Python Developer",
        application_date=date(2026, 10, 30),
        status="Applied",
        notes="Applied through HR email.",
    )

    mock_db.get.return_value = mock_application

    app.dependency_overrides[get_db] = lambda: mock_db

    try:
        response = client.delete("/applications/1")

        assert response.status_code == 200
        
        assert response.json()["message"] == "Job application deleted successfully."

        mock_db.delete.assert_called_once_with(mock_application)
        mock_db.commit.assert_called_once()

    finally:
        app.dependency_overrides.clear()