from bson import ObjectId
from fastapi import APIRouter, HTTPException
from app.database import jobs_collection, applications_collection
from app.schemas import JobCreate


router = APIRouter(
    prefix="/jobs",
    tags=["jobs"]
)

def serialize_job(job):
    return {
        "id": str(job["_id"]),
        "title": job["title"],
        "description": job.get("description"),
        "company_id": job["company_id"],
        "salary_range": job.get("salary_range"),
        "status": job.get("status")
    }

@router.post("")
def create_job(job: JobCreate):
    job_dict = job.model_dump()
    result = jobs_collection.insert_one(job_dict)
    created_job = jobs_collection.find_one({"_id": result.inserted_id})
    return serialize_job(created_job)

@router.get("")
def list_jobs():
    jobs = list(jobs_collection.find())
    return [serialize_job(job) for job in jobs]

@router.get("/{job_id}")
def get_job(job_id: str):
    if not ObjectId.is_valid(job_id):
        raise HTTPException(status_code=400, detail="Invalid job ID")
    job = jobs_collection.find_one({"_id": ObjectId(job_id)})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return serialize_job(job)

@router.delete("/{job_id}")
def delete_job(job_id: str):
    if not ObjectId.is_valid(job_id):
        raise HTTPException(status_code=400, detail="Invalid job id")

    linked_application = applications_collection.find_one({
        "job_id": ObjectId(job_id)
    })

    if linked_application:
        raise HTTPException(
            status_code=409,
            detail="Job cannot be deleted because it has linked applications"
        )

    result = jobs_collection.delete_one({
        "_id": ObjectId(job_id)
    })

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Job not found")

    return {"message": "Job deleted successfully"}