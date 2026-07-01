from bson import ObjectId
from fastapi import APIRouter, HTTPException
from app.database import applications_collection, jobs_collection
from app.schemas import ApplicationCreate, ApplicationStatusUpdate


router = APIRouter(
    prefix="/applications", 
    tags=["applications"]
)

def serialize_application(application):
    return {
        "id": str(application["_id"]),
        "job_id": application["job_id"],
        "status": application["status"],
        "candidate_name": application["candidate_name"],
        "candidate_email": application["candidate_email"],
        "notes": application.get("notes")
    }

@router.post("")
def create_application(application: ApplicationCreate):
    if not ObjectId.is_valid(application.job_id):
        raise HTTPException(status_code=400, detail="Invalid job ID")
    
    job = jobs_collection.find_one({"_id": ObjectId(application.job_id)})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    alreadyApplicated = applications_collection.find_one({
        "job_id": application.job_id,
        "candidate_email": application.candidate_email
    }) 
    if alreadyApplicated:
        raise HTTPException(status_code=409, detail="Candidate has already applied for this job")
    
    application_dict = application.model_dump()
    result = applications_collection.insert_one(application_dict)
    created_application = applications_collection.find_one({"_id": result.inserted_id})
    return serialize_application(created_application)

@router.get("")
def list_applications(
    status: str | None = None,
    candidate_email: str | None = None
):
    query = {}

    if status:
        query["status"] = status

    if candidate_email:
        query["candidate_email"] = candidate_email

    applications = applications_collection.find(query)

    return [
        serialize_application(application)
        for application in applications
    ]

@router.patch("/{application_id}/status")
def update_application_status(
    application_id: str,
    payload: ApplicationStatusUpdate
):
    if not ObjectId.is_valid(application_id):
        raise HTTPException(status_code=400, detail="Invalid application id")

    result = applications_collection.update_one(
        {"_id": ObjectId(application_id)},
        {"$set": {"status": payload.status}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Application not found")

    updated_application = applications_collection.find_one({
        "_id": ObjectId(application_id)
    })

    return serialize_application(updated_application)

@router.delete("/{application_id}")
def delete_application(application_id: str):
    if not ObjectId.is_valid(application_id):
        raise HTTPException(status_code=400, detail="Invalid application id")

    result = applications_collection.delete_one({
        "_id": ObjectId(application_id)
    })

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Application not found")

    return {"message": "Application deleted successfully"}