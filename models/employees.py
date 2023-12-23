from pydantic import BaseModel
from typing import List
from datetime import datetime

class Employee(BaseModel):
    name: str
    email: str
    department: str
    position: str
    date_of_joining: datetime

class EmployeeCreate(Employee):
    pass

class EmployeeUpdate(BaseModel):
    name: str = None
    department: str = None
    position: str = None
    date_of_joining: datetime = None

class Department(BaseModel):
    name: str
    employees: List[Employee]

class AnalyticsResult(BaseModel):
    # Define models for analytics results if needed
    pass

class User(BaseModel):
    username: str
    password: str
    role: str

class AuditLogEntry(BaseModel):
    timestamp: datetime
    user_id: str
    action: str
    details: str

class APIResponse(BaseModel):
    message: str
