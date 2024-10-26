import os
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, Body, HTTPException, status, Query, Depends, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import motor.motor_asyncio
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
import secrets
from utils import TokenService
import logging
from models import *
import uvicorn
from contextlib import asynccontextmanager
from environs import Env
from mangum import Mangum

import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = None


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     global client
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)  # Set the new loop as the current loop
#     client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
#     yield
#     # Cleanup actions on shutdown
#     if client is not None:
#         client.close()


app = FastAPI(
    title="Mental Health API",
    summary="Will handle token generation and form submission",
)


# Configure CORS
origins = [
    "http://localhost:53856",
    "https://medicalhealth.vercel.app",
    "http://127.0.0.1",
    "http://localhost"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.middleware("http")
# async def custom_middleware(request, call_next):
#     try:
#         response = await call_next(request)
#         return response
#     except RuntimeError as e:
#         if "Event loop is closed" in str(e):
#             # Handle the closed loop case
#             loop = asyncio.new_event_loop()
#             asyncio.set_event_loop(loop)
#             response = await call_next(request)
#         return response


env = Env()
env.read_env()
USER_DB = env.dict("BASIC_AUTH", subcast=str)



def reconnect_mongo():
    global client
    if client == None:
        client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
    db = client.medicalhealth
    return db

security = HTTPBasic()


@app.post(
    "/submit/",
    response_description="Submit your response",
    # response_model=EmployeeModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def submit_user_response(
    employee: EmployeeModel = Body(...), token: Optional[str] = Query(None)
):
    """
    Insert a new form record if the provided token is valid and matches the employee ID.
    """

    db  = reconnect_mongo()
    # Check if the token exists and matches the employee ID
    token_entry = await db.get_collection("Token").find_one({"token": token})

    if (
        not token_entry
        or token_entry.get("used", False)
        or token_entry["employee_id"] != employee.Employee_ID
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token or used or employee ID mismatch.",
        )

    await db.get_collection("medical_responses").insert_one(
        {
            **employee.dict(by_alias=True, exclude=["id"]),
            "company": token_entry.get("company", {}).get("companyName"),
        }
    )

    await db.get_collection("Token").update_one(
        {"token": token}, {"$set": {"used": True, "used_at": datetime.now()}}
    )

    return {"message": "Your response has been successfully recorded."}


@app.post(
    "/create_token/{company_name}",
    response_description="Send User tokens",
    response_model=TokenListResponse,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_tokens(
    company_name: str, credentials: HTTPBasicCredentials = Depends(security)
):
    """
    Insert a new employee record associated with a company.

    A unique `id` will be created and provided in the response.
    # TODO: 1. Add a mailer to send it every user
    # TODO: 2. Mark other tokens expire
    """
    # Authentication check
    correct_username = USER_DB.get(credentials.username)
    if not correct_username or correct_username != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    db = reconnect_mongo()
    company = await db.get_collection("Company").find_one({"companyName": company_name})
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")

    employees = company.get("employeeIds", [])
    token_service = TokenService(db)
    async with await db.client.start_session() as session:
        async with session.start_transaction():
            tokens = []
            try:
                for employee_id in employees:
                    token_entry = await token_service.create_token(employee_id, company)
                    # tokens.append(token_entry)
                    tokens.append(
                        TokenResponse(token=token_entry["token"], employee=employee_id)
                    )
                return TokenListResponse(tokens=tokens)
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail="Token creation failed for one or more employees.",
                )


@app.post(
    "/register_company/{company_name}",
    response_description="Register new compnany",
    # response_model=EmployeeIdListModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def register_company(
    company_name: str,
    employees: EmployeeIdListModel,
    credentials: HTTPBasicCredentials = Depends(security),
):
    """Register company in the system"""
    # Authentication check
    correct_username = USER_DB.get(credentials.username)
    if not correct_username or correct_username != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    if not employees.employees:
        raise HTTPException(status_code=422, detail="Employees list cannot be empty or Employee Id can't be less than 5 characters")
    db  = reconnect_mongo()
    company = await db.get_collection("Company").find_one({"companyName": company_name})

    # Verify request
    if company is not None:
        raise HTTPException(
            status_code=404,
            detail="Company is already registered, if you want to update employee use PUT request to update",
        )

    db  = reconnect_mongo()
    # Database Opertation
    result = await db.Company.update_one(
        {"companyName": company_name},
        {"$addToSet": {"employeeIds": {"$each": employees.employees}}},
        upsert=True,  # Create a new document if it doesn't exist
    )

    return {"message": f"{company_name} registered. You can now create tokens"}


@app.put(
    "/register_company/{company_name}",
    response_description="Register new compnany",
    # response_model=EmployeeIdListModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def register_company(
    company_name: str,
    employees: EmployeeIdListModel,
    request: Request,
    credentials: HTTPBasicCredentials = Depends(security),
):
    """Update companies in the system"""
    # Authentication check
    correct_username = USER_DB.get(credentials.username)
    if not correct_username or correct_username != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
        
    if not employees.employees:
        raise HTTPException(status_code=422, detail="Employees list cannot be empty or Employee Id can't be less than 5 characters")

    # Check if mongo connection is establised or not(needed if running in serveless environment)
    db  = reconnect_mongo()
    company = await db.get_collection("Company").find_one({"companyName": company_name})

    # Verify request
    if company is None:
        raise HTTPException(
            status_code=404,
            detail="Company not registered, if you are new please use POST request to register",
        )

    db  = reconnect_mongo()
    #  Database Opertation
    result = await db.Company.update_one(
        {"companyName": company_name},
        {"$addToSet": {"employeeIds": {"$each": employees.employees}}},
        upsert=True,  # Create a new document if it doesn't exist
    )
    return {"message": f"{result.modified_count} employees added to {company_name}"}


@app.post(
    "/auth/login",
    response_description="Authenticaton endpoint",
    # response_model=EmployeeIdListModel,
    status_code=status.HTTP_200_OK,
    response_model_by_alias=False,
)
async def authenticate(
    credentials: HTTPBasicCredentials = Depends(security),
):
    """authentication endpoint"""
    # Authentication check
    correct_username = USER_DB.get(credentials.username)
    if not correct_username or correct_username != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    return {"authinticated": True}


handler = Mangum(app, lifespan="off")
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000)
    
