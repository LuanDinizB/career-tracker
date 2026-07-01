from bson import ObjectId
from fastapi import APIRouter, HTTPException
from app.database import companies_collection
from app.schemas import CompanyCreate
from app.database import companies_collection, jobs_collection

router = APIRouter(
    prefix="/companies",
    tags=["companies"]
)

def serialize_company(company):
    return {
        "id": str(company["_id"]),
        "name": company["name"],
        "website": company.get("website"),
        "description": company.get("description")
    }

@router.post("")
def create_company(company: CompanyCreate):
    company_dict = company.model_dump()
    result = companies_collection.insert_one(company_dict)
    created_company = companies_collection.find_one({"_id": result.inserted_id})
    return serialize_company(created_company)

@router.get("")
def list_companies():
    companies = list(companies_collection.find())
    return [serialize_company(company) for company in companies]

@router.get("/{company_id}")
def get_company(company_id: str):
    if not ObjectId.is_valid(company_id):
        raise HTTPException(status_code=400, detail="Invalid company ID")
    company = companies_collection.find_one({"_id": ObjectId(company_id)})
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return serialize_company(company)


@router.delete("/{company_id}")
def delete_company(company_id: str):
    if not ObjectId.is_valid(company_id):
        raise HTTPException(status_code=400, detail="Invalid company id")

    linked_job = jobs_collection.find_one({
        "company_id": ObjectId(company_id)
    })

    if linked_job:
        raise HTTPException(
            status_code=409,
            detail="Company cannot be deleted because it has linked jobs"
        )

    result = companies_collection.delete_one({
        "_id": ObjectId(company_id)
    })

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Company not found")

    return {"message": "Company deleted successfully"}