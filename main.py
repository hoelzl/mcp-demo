"""
HR System API - A demo application for managing employees with role-based access control.
"""
from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from jose import JWTError, jwt
from passlib.context import CryptContext

# Configuration
SECRET_KEY = "demo-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

app = FastAPI(
    title="HR System API",
    description="A demo HR system with role-based access control",
    version="1.0.0"
)


# Models
class User(BaseModel):
    username: str
    role: str  # "admin", "hr", "employee"
    disabled: bool = False


class UserInDB(User):
    hashed_password: str


class LoginRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class Employee(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    department: str
    position: str
    salary: float
    hire_date: str


class EmployeeCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    department: str
    position: str
    salary: float
    hire_date: str


class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    salary: Optional[float] = None
    hire_date: Optional[str] = None


# In-memory databases
users_db = {
    "admin": UserInDB(
        username="admin",
        role="admin",
        hashed_password=pwd_context.hash("admin123"),
        disabled=False
    ),
    "hr_manager": UserInDB(
        username="hr_manager",
        role="hr",
        hashed_password=pwd_context.hash("hr123"),
        disabled=False
    ),
    "john_doe": UserInDB(
        username="john_doe",
        role="employee",
        hashed_password=pwd_context.hash("employee123"),
        disabled=False
    ),
}

employees_db = {
    1: Employee(
        id=1,
        first_name="John",
        last_name="Doe",
        email="john.doe@company.com",
        department="Engineering",
        position="Software Engineer",
        salary=85000.0,
        hire_date="2023-01-15"
    ),
    2: Employee(
        id=2,
        first_name="Jane",
        last_name="Smith",
        email="jane.smith@company.com",
        department="Human Resources",
        position="HR Manager",
        salary=75000.0,
        hire_date="2022-06-01"
    ),
    3: Employee(
        id=3,
        first_name="Bob",
        last_name="Johnson",
        email="bob.johnson@company.com",
        department="Sales",
        position="Sales Representative",
        salary=65000.0,
        hire_date="2023-09-10"
    ),
}

next_employee_id = 4


# Helper functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(datetime.timezone.utc) + expires_delta
    else:
        expire = datetime.now(datetime.timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
    """
    Authenticate a user by username and password.
    
    BUG: This function has a logical error in the authentication check.
    It returns the user when password verification FAILS instead of when it SUCCEEDS.
    This is intentionally introduced for demonstration purposes.
    """
    user = users_db.get(username)
    if not user:
        return None
    # BUG: The condition is inverted - should be 'if verify_password(...)' not 'if not verify_password(...)'
    if not verify_password(password, user.hashed_password):
        return user
    return None


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = users_db.get(username)
    if user is None:
        raise credentials_exception
    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return User(username=user.username, role=user.role, disabled=user.disabled)


def check_permission(user: User, required_roles: List[str]):
    """Check if user has required role."""
    if user.role not in required_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Access denied. Required role: {', '.join(required_roles)}"
        )


# API Endpoints
@app.get("/")
async def root():
    return {
        "message": "Welcome to HR System API",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.post("/login", response_model=Token)
async def login(login_data: LoginRequest):
    """
    Login endpoint to authenticate users and receive an access token.
    
    Test credentials:
    - admin / admin123 (Admin role)
    - hr_manager / hr123 (HR role)
    - john_doe / employee123 (Employee role)
    """
    user = authenticate_user(login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Get current user information."""
    return current_user


@app.get("/employees", response_model=List[Employee])
async def list_employees(current_user: User = Depends(get_current_user)):
    """
    List all employees.
    Accessible by: admin, hr, employee (all authenticated users)
    """
    return list(employees_db.values())


@app.get("/employees/{employee_id}", response_model=Employee)
async def get_employee(employee_id: int, current_user: User = Depends(get_current_user)):
    """
    Get a specific employee by ID.
    Accessible by: admin, hr, employee (all authenticated users)
    """
    if employee_id not in employees_db:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employees_db[employee_id]


@app.post("/employees", response_model=Employee, status_code=status.HTTP_201_CREATED)
async def create_employee(
    employee_data: EmployeeCreate,
    current_user: User = Depends(get_current_user)
):
    """
    Create a new employee.
    Accessible by: admin, hr only
    """
    check_permission(current_user, ["admin", "hr"])
    
    global next_employee_id
    new_employee = Employee(
        id=next_employee_id,
        **employee_data.dict()
    )
    employees_db[next_employee_id] = new_employee
    next_employee_id += 1
    return new_employee


@app.put("/employees/{employee_id}", response_model=Employee)
async def update_employee(
    employee_id: int,
    employee_data: EmployeeUpdate,
    current_user: User = Depends(get_current_user)
):
    """
    Update an employee.
    Accessible by: admin, hr only
    """
    check_permission(current_user, ["admin", "hr"])
    
    if employee_id not in employees_db:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    employee = employees_db[employee_id]
    update_data = employee_data.dict(exclude_unset=True)
    
    updated_employee = employee.copy(update=update_data)
    employees_db[employee_id] = updated_employee
    return updated_employee


@app.delete("/employees/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(
    employee_id: int,
    current_user: User = Depends(get_current_user)
):
    """
    Delete an employee.
    Accessible by: admin only
    """
    check_permission(current_user, ["admin"])
    
    if employee_id not in employees_db:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    del employees_db[employee_id]
    return None


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
