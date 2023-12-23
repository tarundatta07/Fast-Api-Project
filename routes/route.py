from fastapi import APIRouter, Depends, Query, HTTPException
from bson import ObjectId
from models.employees import Employee
from config.database import collection_name
from schemas.schema import list_serial
from datetime import datetime, timedelta
from typing import List

router = APIRouter()

def validate_object_id(id: str = Depends(ObjectId)):
    return id

# GET REQUEST METHOD
@router.get("/")
async def get_employees():
    employees = list_serial(collection_name.find())
    return employees

# POST REQUEST METHOD
@router.post("/")
async def post_employees(employee: Employee):
    collection_name.insert_one(dict(employee))


@router.put("/{id}")
async def put_employee(id: str, employee: Employee, id_valid: str = Depends(validate_object_id)):
    result = collection_name.find_one_and_update(
        {"_id": id_valid}, {"$set": dict(employee)}
    )
    if result:
        return {"message": "Employee updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Employee not found")

@router.delete("/{id}")
async def delete_employee(id: str, id_valid: str = Depends(validate_object_id)):
    result = collection_name.find_one_and_delete({"_id": id_valid})
    if result:
        return {"message": "Employee deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Employee not found")


# Complex Queries for Employee
@router.get("/employees/search/", response_model=List[Employee])
async def search_employees(
    department: str = Query(None, title="Department"),
    date_of_joining: datetime = Query(None, title="Date of Joining"),
    position: str = Query(None, title="Position"),
):
    query = {}

    if department:
        query["department"] = department

    if date_of_joining:
        query["date_of_joining"] = {"$gte": date_of_joining}

    if position:
        query["position"] = position

    employees = list_serial(collection_name.find(query))
    return employees


# Analytics Endpoints
@router.get("/analytics/employee-count/")
async def department_employee_count():
    pipeline = [
        {"$group": {"_id": "$department", "count": {"$sum": 1}}}
    ]
    result = list_serial(collection_name.aggregate(pipeline))
    return result


# GET AVERAGE TUNURE
@router.get("/analytics/average-tenure/")
async def average_tenure():
    pipeline = [
        {"$match": {"date_of_joining": {"$exists": True}}},
        {"$group": {"_id": None, "average_tenure": {"$avg": {"$subtract": [datetime.now(), "$date_of_joining"]}}}}
    ]
    result = list_serial(collection_name.aggregate(pipeline))
    # print(result)
    if not result:
        raise HTTPException(status_code=404, detail="No data available for average tenure")
    elif "average_tenure" in result[0]:
        return result[0]["average_tenure"]
    else:
        raise HTTPException(status_code=404, detail="Average tenure not available")


@router.get("/analytics/hiring-trends/")
async def hiring_trends(interval: str = "monthly"):
    match_stage = {}
    
    if interval == "monthly":
        match_stage["$match"] = {"date_of_joining": {"$gte": datetime.now() - timedelta(days=30)}}
    elif interval == "yearly":
        match_stage["$match"] = {"date_of_joining": {"$gte": datetime.now() - timedelta(days=365)}}

    pipeline = [
        match_stage,
        {"$group": {"_id": {"$dateToString": {"format": "%Y-%m" if interval == "monthly" else "%Y", "date": "$date_of_joining"}}, "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]
    result = list_serial(collection_name.aggregate(pipeline))
    return result


from skills import identify_skill_gaps

# Sample employee and department skill data
employees_skills = [
    {"python": 3, "sql": 4, "communication": 2},
    {"python": 2, "sql": 3, "teamwork": 5},
    {"python": 1, "communication": 3, "teamwork": 2},  # Added for HR department
]

department_requirements = {
    "IT": {"python": 4, "sql": 3, "communication": 2},
    "HR": {"communication": 3, "teamwork": 4},
}

# Endpoint to get skill gaps by department
@router.get("/skill-gaps")
async def get_skill_gaps():
    skill_gaps = identify_skill_gaps(employees_skills, department_requirements)
    return skill_gaps

