# CareerPilot — Intelligent Job Application & Skill Gap Analyzer

CareerPilot is a Python-based application that helps candidates analyze their skills against job requirements. It extracts skills from resumes, calculates skill-match percentages, identifies missing skills, and recommends areas for improvement.

## Features

- **Resume Parsing:** Extract text and identify skills from PDF resumes.
- **Skill Gap Analysis:** Compare candidate skills with job requirements.
- **Match Percentage:** Calculate how closely a candidate's skills match a job.
- **Learning Recommendations:** Suggest learning priorities for missing skills.
- **Job Management:** Create, view, update, and delete job records.
- **REST API:** Access application functionality through FastAPI endpoints.
- **Database Integration:** Store job information in PostgreSQL.
- **Automated Testing:** Validate application functionality using pytest.

## Technology Stack

- **Language:** Python
- **API Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Resume Processing:** pypdf
- **Validation and Configuration:** Pydantic Settings
- **Testing:** pytest and HTTPX
- **Development Tools:** VS Code, Git, GitHub

## Project Structure

```text
CareerPilot_Python_Project/
├── app/
│   ├── services/
│   │   ├── recommendation_engine.py
│   │   ├── resume_parser.py
│   │   └── skill_analyzer.py
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   └── models.py
├── tests/
│   ├── test_api.py
│   ├── test_recommendation_engine.py
│   ├── test_resume_parser.py
│   └── test_skill_analyzer.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Prerequisites

- Python 3.12 or compatible version
- PostgreSQL
- Git

## Setup and Installation

### 1. Clone the repository

```bash
git clone https://github.com/Mayank14-03/CareerPilot.git
cd CareerPilot
```

### 2. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root and configure the database connection using your local PostgreSQL credentials.

Example format:

```env
DATABASE_URL=postgresql+psycopg://careerpilot_user:YOUR_PASSWORD@localhost:5432/careerpilot_db
```

Replace `YOUR_PASSWORD` with your own PostgreSQL password. Never commit your actual `.env` file or credentials to GitHub.

### 5. Start the application

```powershell
python -m uvicorn app.main:app --reload
```

The API will be available at:

- **Base URL:** http://127.0.0.1:8000
- **Interactive API Documentation:** http://127.0.0.1:8000/docs
- **Health Check:** http://127.0.0.1:8000/health

Ensure PostgreSQL is running and the database is configured before starting the application.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Home endpoint |
| GET | `/health` | Health check |
| POST | `/resume/extract` | Extract information from a resume |
| POST | `/analyze-skills` | Analyze candidate skills |
| POST | `/jobs` | Create a job |
| GET | `/jobs` | List jobs |
| GET | `/jobs/{job_id}` | Get a job by ID |
| PUT | `/jobs/{job_id}` | Update a job |
| DELETE | `/jobs/{job_id}` | Delete a job |
| POST | `/jobs/{job_id}/analyze` | Analyze skills against a saved job |
| POST | `/jobs/{job_id}/analyze-resume` | Analyze a resume against a saved job |

## Run Tests

Run the automated test suite from the project root:

```powershell
python -m pytest -v
```

The current test suite contains 16 passing tests.

## Learning Outcomes

This project demonstrates practical experience with:

- Python application development
- REST API development using FastAPI
- PostgreSQL database integration
- PDF text extraction and skill identification
- Set-based skill matching and match-percentage calculation
- Recommendation logic
- Automated testing
- Git and GitHub version control

## Future Enhancements

- Add a web-based user interface.
- Improve resume parsing and skill recognition.
- Integrate job-board data sources.
- Add user authentication and candidate profiles.
- Expand personalized learning recommendations.

## Author

**Mayank Korde**

MCA Graduate | Python | FastAPI | PostgreSQL | AWS

GitHub: [Mayank14-03](https://github.com/Mayank14-03)

---

*CareerPilot is a portfolio project developed for learning and demonstrating Python development skills.*