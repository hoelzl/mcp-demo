# HR System API - MCP Demo

A demo repository to illustrate the GitHub MCP server, featuring a FastAPI-based HR management system with role-based access control.

## Overview

This is a Python application that simulates an HR system for managing employees of a fictitious company. The system includes:

- **Authentication & Authorization**: Login functionality with JWT tokens and role-based permissions
- **Employee Management**: CRUD operations for employee records
- **Role-Based Access Control**: Three user roles with different permission levels
  - `admin`: Full access to all operations
  - `hr`: Can view, create, and update employees
  - `employee`: Can only view employee information
- **RESTful API**: Built with FastAPI for modern, fast API development
- **CI/CD**: GitHub Actions workflow for continuous integration

## Demo Credentials

The system comes with three pre-configured users:

| Username    | Password     | Role     | Permissions                          |
|-------------|--------------|----------|--------------------------------------|
| admin       | admin123     | admin    | Full access (view, create, update, delete) |
| hr_manager  | hr123        | hr       | View, create, update employees       |
| john_doe    | employee123  | employee | View employees only                  |

## Installation

1. Clone the repository:
```bash
git clone https://github.com/hoelzl/mcp-demo.git
cd mcp-demo
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the server:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## Usage Examples

### 1. Login to get an access token

```bash
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 2. Get current user information

```bash
curl -X GET "http://localhost:8000/users/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 3. List all employees

```bash
curl -X GET "http://localhost:8000/employees" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 4. Create a new employee (admin or hr only)

```bash
curl -X POST "http://localhost:8000/employees" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Alice",
    "last_name": "Williams",
    "email": "alice.williams@company.com",
    "department": "Marketing",
    "position": "Marketing Manager",
    "salary": 80000.0,
    "hire_date": "2024-01-15"
  }'
```

### 5. Update an employee (admin or hr only)

```bash
curl -X PUT "http://localhost:8000/employees/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "salary": 90000.0,
    "position": "Senior Software Engineer"
  }'
```

### 6. Delete an employee (admin only)

```bash
curl -X DELETE "http://localhost:8000/employees/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## API Endpoints

| Method | Endpoint              | Description                    | Required Role       |
|--------|-----------------------|--------------------------------|---------------------|
| GET    | /                     | API information                | Public              |
| POST   | /login                | Login and get access token     | Public              |
| GET    | /users/me             | Get current user info          | Any authenticated   |
| GET    | /employees            | List all employees             | Any authenticated   |
| GET    | /employees/{id}       | Get specific employee          | Any authenticated   |
| POST   | /employees            | Create new employee            | admin, hr           |
| PUT    | /employees/{id}       | Update employee                | admin, hr           |
| DELETE | /employees/{id}       | Delete employee                | admin only          |

## Known Issues

⚠️ **Note**: This application contains an intentional bug in the login functionality for demonstration purposes. The bug is documented in the code and will be used to illustrate how the GitHub MCP server can help identify and create issues for bugs.

## Technology Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation using Python type annotations
- **python-jose**: JWT token implementation
- **passlib**: Password hashing and verification
- **uvicorn**: ASGI server for running the application

## CI/CD

The project uses GitHub Actions for continuous integration. The workflow:
- Runs on Python 3.9, 3.10, and 3.11
- Installs dependencies
- Runs linting with Ruff
- Executes tests (when available)
- Performs basic smoke test of the API

## License

MIT License - See LICENSE file for details
