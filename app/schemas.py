from pydantic import BaseModel, EmailStr
from enum import Enum

class ApplicationStatus(str, Enum):
    APPLIED = "applied"
    SCREENING = "screening"
    INTERVIEW = "interview"
    TECHNICAL_TEST = "technical_test"
    REJECTED = "rejected"
    OFFER = "offer"

class CompanyCreate(BaseModel):
    name: str
    website: str | None = None
    description: str | None = None

class CompanyResponse(BaseModel):
    id: int
    name: str
    website: str | None = None
    description: str | None = None

class JobCreate(BaseModel):
    title: str
    description: str | None = None
    company_id: str
    salary_range: str | None = None
    description: str | None = None
    status: str | None = None

class ApplicationCreate(BaseModel):
    job_id: str
    status: ApplicationStatus = ApplicationStatus.APPLIED
    candidate_name: str
    candidate_email: EmailStr
    notes: str | None = None

class ApplicationStatusUpdate(BaseModel):
    status: ApplicationStatus
