from fastapi import APIRouter
from app.database import applications_collection

router = APIRouter(
    prefix="/metrics",
    tags=["metrics"]
)


@router.get("/summary")
def get_summary():
    total_applications = applications_collection.count_documents({})

    pipeline = [
        {
            "$group": {
                "_id": "$status",
                "count": {"$sum": 1}
            }
        }
    ]

    status_results = applications_collection.aggregate(pipeline)

    by_status = {
        item["_id"]: item["count"]
        for item in status_results
    }

    return {
        "total_applications": total_applications,
        "by_status": by_status
    }