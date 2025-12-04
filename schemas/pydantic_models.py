"""
Pydantic models for request and response validation
"""
from datetime import datetime
from typing import Optional, List, Any, Dict
from pydantic import BaseModel, Field, EmailStr, validator


# ==================== REQUEST MODELS ====================

class LoginRequest(BaseModel):
    """Request model for user login"""
    username: str = Field(..., min_length=1, description="Username")
    password: str = Field(..., min_length=1, description="Password")


class AddUserRequest(BaseModel):
    """Request model for adding a new user"""
    first_name: str = Field(..., min_length=1, description="First name")
    last_name: str = Field(..., min_length=1, description="Last name")
    middle_name: Optional[str] = Field(None, description="Middle name")
    mobile_number: Optional[str] = Field(None, description="Mobile number")
    email: EmailStr = Field(..., description="Email address")
    dob_dtm: str = Field(..., description="Date of birth")
    introduction: str = Field(..., description="Introduction")
    address: str = Field(..., description="Address")
    city_id: int = Field(..., gt=0, description="City ID")
    pincode: int = Field(..., gt=0, description="Pincode")
    gender: str = Field(..., description="Gender")
    user_name: str = Field(..., min_length=1, description="Username")
    password: str = Field(..., min_length=1, description="Password")
    profile_image_id: Optional[int] = Field(None, description="Profile image ID")
    is_blocked: Optional[bool] = Field(False, description="Is blocked")
    blocked_on: Optional[int] = Field(None, description="Blocked on timestamp")
    registered_on: Optional[str] = Field(None, description="Registration date")
    last_login_on: Optional[str] = Field(None, description="Last login date")


class UpdateUserRequest(BaseModel):
    """Request model for updating a user"""
    id: int = Field(..., gt=0, description="User ID")
    first_name: str = Field(..., min_length=1, description="First name")
    last_name: str = Field(..., min_length=1, description="Last name")
    middle_name: Optional[str] = Field(None, description="Middle name")
    mobile_number: Optional[str] = Field(None, description="Mobile number")
    email: EmailStr = Field(..., description="Email address")
    dob_dtm: str = Field(..., description="Date of birth")
    introduction: str = Field(..., description="Introduction")
    address: str = Field(..., description="Address")
    city_id: int = Field(..., gt=0, description="City ID")
    pincode: int = Field(..., gt=0, description="Pincode")
    gender: str = Field(..., description="Gender")
    user_name: str = Field(..., min_length=1, description="Username")
    password: Optional[str] = Field(None, description="Password")
    profile_image_id: Optional[int] = Field(None, description="Profile image ID")
    is_blocked: Optional[bool] = Field(False, description="Is blocked")
    blocked_on: Optional[int] = Field(None, description="Blocked on timestamp")
    registered_on: Optional[str] = Field(None, description="Registration date")
    last_login_on: Optional[str] = Field(None, description="Last login date")


class AddOrganizationRequest(BaseModel):
    """Request model for adding a user organization"""
    name: str = Field(..., min_length=1, description="Organization name")
    address: str = Field(..., description="Address")
    city_id: int = Field(..., gt=0, description="City ID")
    duration_from: str = Field(..., description="Duration from date")
    duration_to: Optional[str] = Field(None, description="Duration to date")
    is_current_organization: bool = Field(..., description="Is current organization")
    user_id: int = Field(..., gt=0, description="User ID")
    team_id: int = Field(..., gt=0, description="Team ID")
    position_id: int = Field(..., gt=0, description="Position ID")


class UpdateOrganizationRequest(BaseModel):
    """Request model for updating a user organization"""
    id: int = Field(..., gt=0, description="Organization ID")
    name: str = Field(..., min_length=1, description="Organization name")
    address: str = Field(..., description="Address")
    city_id: int = Field(..., gt=0, description="City ID")
    duration_from: str = Field(..., description="Duration from date")
    duration_to: Optional[str] = Field(None, description="Duration to date")
    is_current_organization: bool = Field(..., description="Is current organization")
    user_id: int = Field(..., gt=0, description="User ID")
    team_id: int = Field(..., gt=0, description="Team ID")
    position_id: int = Field(..., gt=0, description="Position ID")


class UploadProfileRequest(BaseModel):
    """Request model for uploading profile"""
    username: str = Field(..., min_length=1, description="Username")


# ==================== RESPONSE MODELS ====================

class StandardResponse(BaseModel):
    """Standard response model"""
    status: str = Field(..., description="Status: success, error, or fail")
    message: str = Field(..., description="Response message")
    data: Optional[Any] = Field(None, description="Response data")


class LoginResponse(BaseModel):
    """Response model for login"""
    status: str = Field(..., description="Status")
    message: str = Field(..., description="Message")
    auth_token: Optional[str] = Field(None, description="Authentication token")
    user_id: Optional[int] = Field(None, description="User ID")


class UserData(BaseModel):
    """User data model for responses"""
    id: Optional[int] = None
    username: Optional[str] = None
    user_name: Optional[str] = None
    email: Optional[str] = None
    active: Optional[bool] = None
    created_at: Optional[datetime] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    mobile_number: Optional[str] = None
    organizations: Optional[List[Dict[str, Any]]] = None

    class Config:
        from_attributes = True
        extra = 'ignore'  # Ignore extra fields when creating from dict
        # Pydantic v2 automatically serializes datetime to ISO format


class UserStatusResponse(BaseModel):
    """Response model for user status"""
    status: str = Field(..., description="Status")
    data: UserData = Field(..., description="User data")


class UsersListResponse(BaseModel):
    """Response model for users list"""
    status: str = Field(..., description="Status")
    data: Dict[str, List[UserData]] = Field(..., description="Users data")


class OrganizationResponse(BaseModel):
    """Response model for organization operations"""
    status: str = Field(..., description="Status")
    message: str = Field(..., description="Message")
    data: Optional[Dict[str, Any]] = Field(None, description="Organization data")


# ==================== ATTENDANCE MODELS ====================

class AttendanceData(BaseModel):
    """Attendance data model for responses"""
    id: Optional[str] = None
    employee_id: Optional[str] = None
    clock_in: Optional[datetime] = None
    clock_out: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        extra = 'ignore'


class AttendanceResponse(BaseModel):
    """Response model for attendance operations"""
    status: str = Field(..., description="Status")
    message: str = Field(..., description="Message")
    data: Optional[AttendanceData] = Field(None, description="Attendance data")

