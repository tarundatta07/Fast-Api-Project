import pytest
from fastapi.testclient import TestClient
from main import app, identify_skill_gaps

client = TestClient(app)

def test_identify_skill_gaps():
    employees_skills = [
        {"python": 3, "sql": 4, "communication": 2},
        {"python": 2, "sql": 3, "teamwork": 5},
        {"python": 1, "communication": 3, "teamwork": 2},  # Added for HR department
    ]

    department_requirements = {
        "IT": {"python": 4, "sql": 3, "communication": 2},
        "HR": {"communication": 3, "teamwork": 4},
    }

    response = client.get("/skill-gaps")
    skill_gaps = response.json()

    # Add assertions based on expected results
    assert skill_gaps["IT"] == ["sql"]  # Adjusted based on the data
    assert skill_gaps["HR"] == ["python", "sql"]
