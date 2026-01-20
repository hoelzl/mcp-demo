"""
Test employee features using Python 3.10+ match/case syntax.

This test intentionally uses Python 3.10+ features (structural pattern matching)
to demonstrate CI failures on Python 3.9.
"""
import pytest


def get_employee_role_description(role: str) -> str:
    """
    Get a description for an employee role using Python 3.10+ match/case.
    
    This function uses structural pattern matching which is only available
    in Python 3.10 and later. This will cause the test to fail on Python 3.9.
    """
    match role:
        case "admin":
            return "Administrator with full system access"
        case "hr":
            return "HR Manager with employee management access"
        case "employee":
            return "Regular employee with view-only access"
        case _:
            return "Unknown role"


def test_admin_role_description():
    """Test admin role description."""
    result = get_employee_role_description("admin")
    assert result == "Administrator with full system access"


def test_hr_role_description():
    """Test HR role description."""
    result = get_employee_role_description("hr")
    assert result == "HR Manager with employee management access"


def test_employee_role_description():
    """Test employee role description."""
    result = get_employee_role_description("employee")
    assert result == "Regular employee with view-only access"


def test_unknown_role_description():
    """Test unknown role description."""
    result = get_employee_role_description("guest")
    assert result == "Unknown role"


def calculate_employee_status(years_of_service: int) -> str:
    """
    Calculate employee status based on years of service using match/case.
    
    This function also uses Python 3.10+ structural pattern matching.
    """
    match years_of_service:
        case years if years < 1:
            return "New hire"
        case years if 1 <= years < 3:
            return "Junior"
        case years if 3 <= years < 5:
            return "Mid-level"
        case years if 5 <= years < 10:
            return "Senior"
        case _:
            return "Veteran"


def test_employee_status_new_hire():
    """Test status for new hires."""
    assert calculate_employee_status(0) == "New hire"


def test_employee_status_junior():
    """Test status for junior employees."""
    assert calculate_employee_status(2) == "Junior"


def test_employee_status_mid_level():
    """Test status for mid-level employees."""
    assert calculate_employee_status(4) == "Mid-level"


def test_employee_status_senior():
    """Test status for senior employees."""
    assert calculate_employee_status(7) == "Senior"


def test_employee_status_veteran():
    """Test status for veteran employees."""
    assert calculate_employee_status(15) == "Veteran"
