
# CareerPilot — Intelligent Job Application & Skill Gap Analyzer

CareerPilot is a Python-based job application tracking and skill gap analysis platform built using FastAPI and PostgreSQL.

It helps candidates manage job applications, extract skills from PDF resumes, compare their skills with job requirements, calculate skill-match percentages, identify missing skills, and receive learning recommendations.

The project also includes an interactive dashboard to track application statistics and manage job applications.

## Features

## Dashboard Preview

The CareerPilot dashboard provides an overview of job applications, application statuses, and recent activities.

![CareerPilot Dashboard](screenshots/dashboard.png)




## Project Architecture

```mermaid
flowchart TD
    A["User"] --> B["CareerPilot Dashboard<br/>HTML, CSS, JavaScript"]
    B --> C["FastAPI Backend"]

    C --> D["Resume Parser"]
    C --> E["Skill Analyzer"]
    C --> F["Recommendation Engine"]
    C --> G["Job Application APIs"]

    D --> E
    E --> F

    C --> H["SQLAlchemy ORM"]
    H --> I[("PostgreSQL Database")]

    J["Pytest"] -.-> C
```


### Resume & Skill Analysis
- **Resume Parsing:** Extract text and identify skills from PDF resumes.
- **Skill Gap Analysis:** Compare candidate skills with job requirements.
- **Match Percentage:** Calculate how closely candidate skills match a job.
- **Missing Skills Identification:** Highlight skills that need improvement.
- **Learning Recommendations:** Suggest learning priorities based on missing skills.

### Job Application Management
- **Create Applications:** Add company, job title, application date, status, and notes.
- **View Applications:** Retrieve saved job application records.
- **Update Applications:** Edit existing application details.
- **Delete Applications:** Remove application records.
- **Application Statistics:** Track total applications and application statuses.

### Interactive Dashboard
- View total applications and status-wise counts.
- Visualize application status through a chart.
- Add, edit, and delete applications directly from the dashboard.
- View recent job application records.

### Backend & Testing
- REST API development using FastAPI.
- PostgreSQL database integration.
- SQLAlchemy ORM.
- Automated API and service testing using pytest.

## Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python 3.12 |
| Backend Framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Data Validation | Pydantic |
| Configuration | Pydantic Settings |
| Resume Processing | pypdf |
| Frontend | HTML, CSS, JavaScript |
| API Documentation | Swagger UI |
| Testing | pytest, HTTPX |
| Tools | VS Code, Git, GitHub |

## Project Structure

```text
CareerPilot_Python_Project/
│
├── app/
│   ├── services/
│   │   ├── recommendation_engine.py
│   │   ├── resume_parser.py
│   │   └── skill_analyzer.py
│   │
│   ├── static/
│   │   └── style.css
│   │
│   ├── templates/
│   │   └── dashboard.html
│   │
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   └── models.py
│
├── tests/
│   ├── test_api.py
│   ├── test_recommendation_engine.py
│   ├── test_resume_parser.py
│   └── test_skill_analyzer.py
│
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

### 1. Clone the Repository

```bash
git clone https://github.com/Mayank14-03/CareerPilot.git

cd CareerPilot
```

### 2. Create and Activate Virtual Environment

Windows PowerShell:

```powershell
python -m venv .venv

.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root.

Configure your PostgreSQL database connection:

```env
DATABASE_URL=postgresql+psycopg://careerpilot_user:YOUR_PASSWORD@localhost:5432/careerpilot_db
```

Replace `YOUR_PASSWORD` with your local PostgreSQL password.

Ensure that:
- PostgreSQL is running.
- The database exists.
- The configured database user has the required permissions.

**Important:** Never commit your actual `.env` file or database credentials to GitHub.

### 5. Start the Application

```powershell
python -m uvicorn app.main:app --reload
```

The application will be available at:

| Resource | URL |
|---|---|
| Base API | http://127.0.0.1:8000 |
| Interactive API Documentation | http://127.0.0.1:8000/docs |
| Health Check | http://127.0.0.1:8000/health |
| Dashboard | http://127.0.0.1:8000/dashboard |

## API Endpoints

### General & Resume APIs

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Home endpoint |
| GET | `/health` | Health check |
| POST | `/resume/extract` | Extract information from a resume |
| POST | `/analyze-skills` | Analyze candidate skills |

### Job Management APIs

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/jobs` | Create a job |
| GET | `/jobs` | List jobs |
| GET | `/jobs/{job_id}` | Get a job by ID |
| PUT | `/jobs/{job_id}` | Update a job |
| DELETE | `/jobs/{job_id}` | Delete a job |
| POST | `/jobs/{job_id}/analyze` | Analyze skills against a saved job |
| POST | `/jobs/{job_id}/analyze-resume` | Analyze a resume against a saved job |

### Job Application APIs

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/applications` | Create a job application |
| GET | `/applications` | List job applications |
| GET | `/applications/{application_id}` | Get an application by ID |
| PUT | `/applications/{application_id}` | Update an application |
| DELETE | `/applications/{application_id}` | Delete an application |
| GET | `/applications/stats` | Get application statistics |

### Dashboard

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/dashboard` | Access the interactive dashboard |

## Run Automated Tests

Run the test suite from the project root:

```powershell
python -m pytest -v
```

**Latest test result: 23 passed.**

Test coverage includes:
- API endpoint testing.
- Job application CRUD operations.
- Application statistics.
- Resume skill extraction.
- Skill gap analysis.
- Skill-based recommendations.

## Learning Outcomes

This project demonstrates practical experience with:

- Python application development.
- REST API development using FastAPI.
- PostgreSQL database integration.
- SQLAlchemy ORM.
- PDF text extraction and skill identification.
- Skill matching and match-percentage calculation.
- Recommendation engine development.
- HTML, CSS, and JavaScript dashboard development.
- CRUD operations.
- Automated testing using pytest.
- Git and GitHub version control.

## Future Enhancements

- Add user authentication and candidate profiles.
- Improve resume parsing and skill recognition.
- Integrate job-board data sources.
- Expand personalized learning recommendations.

## Author

**Mayank Korde**

MCA Graduate | Python | FastAPI | PostgreSQL | AWS

GitHub: [Mayank14-03](https://github.com/Mayank14-03)

---

*CareerPilot is a portfolio project developed for learning and demonstrating Python backend development skills.*
