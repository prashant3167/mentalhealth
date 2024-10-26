from typing import Optional, List

from pydantic import BaseModel, Field, constr, conlist, model_validator
from datetime import datetime
from typing_extensions import Annotated

PyObjectId = str


class EmployeeModel(BaseModel):
    """
    Container for a single employee record.
    """

    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    Employee_ID: str = Field(...)
    Age: str = Field(...)
    Gender: str = Field(...)
    Job_Role: str = Field(...)
    Industry: str = Field(...)
    Work_Location: str = Field(...)
    Years_of_Experience: str = Field(...)
    Hours_Worked_Per_Week: str = Field(...)
    Number_of_Virtual_Meetings: str = Field(...)
    Work_Life_Balance_Rating: str = Field(...)
    Stress_Level: str = Field(...)
    Mental_Health_Condition: str = Field(...)
    Access_to_Mental_Health_Resources: str = Field(...)
    Productivity_Change: str = Field(...)
    Social_Isolation_Rating: str = Field(...)
    Company_Support_for_Remote_Work: str = Field(...)
    Satisfaction_with_Remote_Work: str = Field(...)
    Physical_Activity: str = Field(...)
    Sleep_Quality: str = Field(...)
    Region: str = Field(...)
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(), exclude=False, include_in_schema=False
    )

    class Config:
        from_attributes = True
        exclude = {"created_at"}


class EmployeeCollection(BaseModel):
    """
    A container holding a list of `EmployeeModel` instances.
    """

    employees: List[EmployeeModel]


class EmployeeIdListModel(BaseModel):
    """
    Container for a multiple employee records.
    """

    employees: conlist(
        Annotated[
            str,
            constr(strip_whitespace=True, min_length=5),
        ],
        min_length=1,  # Ensure the list has at least one element
    )
    
    @model_validator(mode='before')  # Using the new @model_validator
    def check_non_empty_strings(cls, values):
        employees = values.get('employees', [])
        # Ensure that there are no empty strings
        if any(employee == '' for employee in employees):
            raise ValueError("Employees list contains empty strings. Empty strings are not allowed.")
        return values

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    token: str
    employee: str


class TokenListResponse(BaseModel):
    tokens: List[TokenResponse]


class LoginItem(BaseModel):
    username: str
    password: str
