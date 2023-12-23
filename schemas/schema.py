def individual_serial(employee) -> dict:
    return {
        "id": str(employee["_id"]),
        "name": employee.get("name", ""),
        "email": employee.get("email", ""),
        "department": employee.get("department", ""),
        "position": employee.get("position", ""),
        "date_of_joining": employee.get("date_of_joining", ""),
    }


def list_serial(employees) -> list:
    return [individual_serial(employee) for employee in employees]