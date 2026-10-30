from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Job, JobApplication  
from app.services.skill_analyzer import analyze_skills
from app.services.resume_parser import extract_skills
from app.services.recommendation_engine import generate_recommendations

from io import BytesIO
from pypdf import PdfReader
from datetime import date
from typing import Literal


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CareerPilot API",
    description="Job Application Tracker and Skill Gap Analyzer",
    version="1.0.0",
)


class SkillAnalysisRequest(BaseModel):
    candidate_skills: list[str]
    required_skills: list[str]


class JobCreate(BaseModel):
    company_name: str = Field(min_length=1, max_length=100)
    job_title: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1)
    required_skills: list[str] = Field(min_length=1)

class JobApplicationCreate(BaseModel):
    company_name: str = Field(min_length=1, max_length=100)
    job_title: str = Field(min_length=1, max_length=100)
    application_date: date = Field(default_factory=date.today)
    status: Literal["Applied", "Interview", "Rejected", "Offer"] = "Applied"
    notes: str | None = None


@app.get("/")
def home():
    return {
        "message": "Welcome to CareerPilot!",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "CareerPilot",
    }


@app.post("/resume/extract")
async def extract_resume_text(
    file: UploadFile = File(...),
):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF file.",
        )

    content = await file.read()

    if not content:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty.",
        )

    try:
        reader = PdfReader(BytesIO(content))

        if reader.is_encrypted:
            raise HTTPException(
                status_code=400,
                detail="Encrypted PDFs are not supported.",
            )

        extracted_text = "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        ).strip()

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Could not read this PDF. Please upload a valid PDF.",
        )

    if not extracted_text:
        raise HTTPException(
            status_code=422,
            detail="No readable text found in the PDF.",
        )
    detected_skills = extract_skills(extracted_text)

    return {
        "filename": file.filename,
        "page_count": len(reader.pages),
        "extracted_text": extracted_text,
        "detected_skills": detected_skills,
        "total_skills_found": len(detected_skills),
    }
    



@app.post("/analyze-skills")
def skill_analysis(request: SkillAnalysisRequest):
    return analyze_skills(
        request.candidate_skills,
        request.required_skills,
    )


@app.post("/jobs", status_code=201)
def create_job(
    job: JobCreate,
    db: Session = Depends(get_db),
):
    job_data = job.model_dump()
    job_data["company_name"] = job_data["company_name"].strip()
    job_data["job_title"] = job_data["job_title"].strip()

    if not job_data["company_name"] or not job_data["job_title"]:
        raise HTTPException(
            status_code=422,
            detail="Company name and job title cannot be blank.",
        )

    db_job = Job(**job_data)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)

    return db_job

@app.post("/applications", status_code=201)
def create_application(
    application: JobApplicationCreate,
    db: Session = Depends(get_db),
):
    application_data = application.model_dump()

    application_data["company_name"] = application_data["company_name"].strip()
    application_data["job_title"] = application_data["job_title"].strip()

    if not application_data["company_name"] or not application_data["job_title"]:
        raise HTTPException(
            status_code=422,
            detail="Company name and job title cannot be blank.",
        )

    db_application = JobApplication(**application_data)

    db.add(db_application)
    db.commit()
    db.refresh(db_application)

    return db_application

@app.get("/applications")
def list_applications(
    db: Session = Depends(get_db),
):
    return (
        db.query(JobApplication)
        .order_by(JobApplication.id.desc())
        .all()
    )

@app.get("/applications/{application_id}")
def get_application(
    application_id: int,
    db: Session = Depends(get_db),
):
    application = db.get(JobApplication, application_id)

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Job application not found.",
        )

    return application

class JobApplicationUpdate(BaseModel):
    company_name: str = Field(min_length=1, max_length=100)
    job_title: str = Field(min_length=1, max_length=100)
    application_date: date
    status: Literal["Applied", "Interview", "Rejected", "Offer"]
    notes: str | None = None


@app.put("/applications/{application_id}")
def update_application(
    application_id: int,
    updated_application: JobApplicationUpdate,
    db: Session = Depends(get_db),
):
    application = db.get(JobApplication, application_id)

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Job application not found.",
        )

    application_data = updated_application.model_dump()
    application_data["company_name"] = application_data["company_name"].strip()
    application_data["job_title"] = application_data["job_title"].strip()

    if not application_data["company_name"] or not application_data["job_title"]:
        raise HTTPException(
            status_code=422,
            detail="Company name and job title cannot be blank.",
        )

    for field, value in application_data.items():
        setattr(application, field, value)

    db.commit()
    db.refresh(application)

    return application

@app.delete("/applications/{application_id}")
def delete_application(
    application_id: int,
    db: Session = Depends(get_db),
):
    application = db.get(JobApplication, application_id)

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Job application not found.",
        )

    db.delete(application)
    db.commit()

    return {
        "message": "Job application deleted successfully.",
        "application_id": application_id,
    }

@app.get("/jobs")
def list_jobs(db: Session = Depends(get_db)):
    return db.query(Job).order_by(Job.id).all()


@app.get("/jobs/{job_id}")
def get_job(
    job_id: int,
    db: Session = Depends(get_db),
):
    job = db.get(Job, job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found.",
        )

    return job


class JobSkillAnalysisRequest(BaseModel):
    candidate_skills: list[str] = Field(min_length=1)


@app.post("/jobs/{job_id}/analyze")
def analyze_job_skills(
    job_id: int,
    request: JobSkillAnalysisRequest,
    db: Session = Depends(get_db),
):
    job = db.get(Job, job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found.",
        )

    result = analyze_skills(
        request.candidate_skills,
        job.required_skills,
    )

    return {
        "job_id": job.id,
        "company_name": job.company_name,
        "job_title": job.job_title,
        **result,
    }



@app.put("/jobs/{job_id}")
def update_job(
    job_id: int,
    updated_job: JobCreate,
    db: Session = Depends(get_db),
):
    db_job = db.get(Job, job_id)

    if db_job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found.",
        )

    job_data = updated_job.model_dump()
    job_data["company_name"] = job_data["company_name"].strip()
    job_data["job_title"] = job_data["job_title"].strip()

    if not job_data["company_name"] or not job_data["job_title"]:
        raise HTTPException(
            status_code=422,
            detail="Company name and job title cannot be blank.",
        )

    for field, value in job_data.items():
        setattr(db_job, field, value)

    db.commit()
    db.refresh(db_job)

    return db_job


@app.delete("/jobs/{job_id}")
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
):
    db_job = db.get(Job, job_id)

    if db_job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found.",
        )

    db.delete(db_job)
    db.commit()

    return {
        "message": "Job deleted successfully.",
        "job_id": job_id,
    }



@app.post("/jobs/{job_id}/analyze-resume")
async def analyze_resume_for_job(
    job_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # Validate the uploaded file
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF file.",
        )

    content = await file.read()

    if not content:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty.",
        )

    # Find the requested job
    job = db.get(Job, job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found.",
        )

    # Extract text from the PDF
    try:
        reader = PdfReader(BytesIO(content))

        if reader.is_encrypted:
            raise HTTPException(
                status_code=400,
                detail="Encrypted PDFs are not supported.",
            )

        extracted_text = "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        ).strip()

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Could not read this PDF. Please upload a valid PDF.",
        )

    if not extracted_text:
        raise HTTPException(
            status_code=422,
            detail="No readable text found in the PDF.",
        )

    # Detect candidate skills from the resume
    candidate_skills = extract_skills(extracted_text)

    # Compare candidate skills with job requirements
    analysis = analyze_skills(
        candidate_skills,
        job.required_skills,
    )

    # Generate recommendations for missing skills
    recommendations = generate_recommendations(
        analysis["missing_skills"]
    )

    # Return the complete resume analysis
    return {
        "filename": file.filename,
        "job_id": job.id,
        "company_name": job.company_name,
        "job_title": job.job_title,
        "detected_skills": candidate_skills,
        "matched_skills": analysis["matched_skills"],
        "missing_skills": analysis["missing_skills"],
        "match_percentage": analysis["match_percentage"],
        "recommendations": recommendations,
    }
