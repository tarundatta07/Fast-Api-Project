from typing import Dict, List
from collections import Counter

# Assuming your Employee model has a 'skills' field
# Example: {"python": 3, "sql": 4, "communication": 2, ...}
EmployeeSkills = Dict[str, int]

# Function to identify skill gaps for a department
def identify_skill_gaps(employees_skills: List[EmployeeSkills], department_requirements: EmployeeSkills) -> Dict[str, List[str]]:
    department_skill_gaps = {}

    # Count the frequency of each skill across all employees
    skill_counts = Counter(skill for employee_skills in employees_skills for skill in employee_skills.keys())

    # Calculate the missing skills for each department
    for department, requirements in department_requirements.items():
        required_skills = set(requirements.keys())
        available_skills = set(skill_counts.keys())
        missing_skills = required_skills - available_skills

        # Sort missing skills by frequency
        sorted_missing_skills = sorted(missing_skills, key=lambda skill: skill_counts[skill], reverse=True)

        department_skill_gaps[department] = sorted_missing_skills

    return department_skill_gaps
