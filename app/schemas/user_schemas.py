"""
Pydantic schemas for User, Profile, and Authentication endpoints.
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, validator
from app.schemas.common_schemas import TimestampMixin, PhoneNumber


# ==================== AUTHENTICATION ====================

class LoginRequest(BaseModel):
    """User login request"""
    email: EmailStr
    password: str = Field(..., min_length=6)
    
    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "password123"
            }
        }


class RegisterRequest(BaseModel):
    """User registration request"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)
    phone: Optional[str] = None
    role: str = "tourist"
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "john@example.com",
                "password": "SecurePass123!",
                "confirm_password": "SecurePass123!",
                "phone": "+1234567890",
                "role": "tourist"
            }
        }


class PasswordChangeRequest(BaseModel):
    """Password change request"""
    old_password: str
    new_password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('New passwords do not match')
        return v


class PasswordResetRequest(BaseModel):
    """Password reset request"""
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Password reset confirmation"""
    token: str
    new_password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Passwords do not match')
        return v


class EmailVerificationRequest(BaseModel):
    """Email verification request"""
    email: EmailStr


class EmailVerificationConfirm(BaseModel):
    """Email verification confirmation"""
    token: str


class PhoneVerificationRequest(BaseModel):
    """Phone verification request"""
    phone: str


class PhoneVerificationConfirm(BaseModel):
    """Phone verification confirmation"""
    phone: str
    otp: str = Field(..., min_length=6, max_length=6)


# ==================== USER PROFILE ====================

class UserProfileBase(BaseModel):
    """Base user profile"""
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    gender: Optional[str] = None
    nationality: Optional[str] = None
    passport_number: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    blood_group: Optional[str] = None
    allergies: Optional[str] = None
    medical_conditions: Optional[str] = None
    emergency_medications: Optional[str] = None


class UserProfileCreate(UserProfileBase):
    """Create user profile"""
    pass


class UserProfileUpdate(UserProfileBase):
    """Update user profile"""
    preferred_language: Optional[str] = "en"
    two_factor_enabled: Optional[bool] = False


class UserProfileResponse(UserProfileBase, TimestampMixin):
    """User profile response"""
    id: int
    user_id: int
    profile_complete: bool
    identity_verified: bool
    preferred_language: str
    two_factor_enabled: bool
    
    class Config:
        from_attributes = True


# ==================== TOURIST PROFILE ====================

class TouristProfileCreate(UserProfileCreate):
    """Create tourist profile"""
    current_destination: Optional[str] = None
    travel_dates_from: Optional[datetime] = None
    travel_dates_to: Optional[datetime] = None
    accommodation_address: Optional[str] = None
    accommodation_phone: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    emergency_contact_email: Optional[EmailStr] = None


class TouristProfileUpdate(TouristProfileCreate):
    """Update tourist profile"""
    pass


# ==================== SERVICE PROVIDER PROFILE ====================

class ServiceProviderProfileCreate(UserProfileCreate):
    """Create service provider profile"""
    organization_name: str
    organization_license: str
    organization_address: str
    organization_website: Optional[str] = None
    registration_number: str
    

class ServiceProviderProfileUpdate(ServiceProviderProfileCreate):
    """Update service provider profile"""
    organization_name: Optional[str] = None
    organization_license: Optional[str] = None
    organization_address: Optional[str] = None
    registration_number: Optional[str] = None


# ==================== EMERGENCY CONTACTS ====================

class EmergencyContactBase(BaseModel):
    """Base emergency contact"""
    name: str = Field(..., max_length=100)
    relationship: Optional[str] = None
    phone: str = Field(..., max_length=20)
    email: Optional[EmailStr] = None
    country_code: str = "+1"
    is_primary: bool = False


class EmergencyContactCreate(EmergencyContactBase):
    """Create emergency contact"""
    notify_on_sos: bool = True
    notify_on_incident: bool = False
    notify_on_geofence: bool = False


class EmergencyContactUpdate(BaseModel):
    """Update emergency contact"""
    name: Optional[str] = None
    relationship: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    country_code: Optional[str] = None
    is_primary: Optional[bool] = None
    notify_on_sos: Optional[bool] = None
    notify_on_incident: Optional[bool] = None
    notify_on_geofence: Optional[bool] = None
    is_active: Optional[bool] = None


class EmergencyContactResponse(EmergencyContactBase, TimestampMixin):
    """Emergency contact response"""
    id: int
    user_id: int
    is_active: bool
    verified: bool
    
    class Config:
        from_attributes = True


# ==================== USER ====================

class UserBase(BaseModel):
    """Base user"""
    username: str
    email: EmailStr
    phone: Optional[str] = None
    role: str


class UserCreate(UserBase):
    """Create user"""
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    """Update user"""
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


class UserResponse(UserBase, TimestampMixin):
    """User response"""
    id: int
    is_active: bool
    is_verified: bool
    email_verified_at: Optional[datetime] = None
    phone_verified_at: Optional[datetime] = None
    is_superuser: bool
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class UserDetailResponse(UserResponse):
    """User detail response with profile"""
    profile: Optional[UserProfileResponse] = None
    emergency_contacts: List[EmergencyContactResponse] = []


class UserListResponse(BaseModel):
    """User list response"""
    id: int
    username: str
    email: str
    role: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ==================== AUTHENTICATION RESPONSES ====================

class LoginResponse(BaseModel):
    """Login response"""
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


class RegisterResponse(BaseModel):
    """Register response"""
    user: UserResponse
    message: str = "Registration successful. Please verify your email."
    verification_required: bool = True


class AuthenticatedUserResponse(BaseModel):
    """Authenticated user response"""
    user: UserDetailResponse
    role: str
    permissions: List[str] = []


# ==================== TWO-FACTOR AUTHENTICATION ====================

class TwoFactorSetupRequest(BaseModel):
    """Two-factor setup request"""
    method: str = Field(..., pattern="^(authenticator|sms)$")


class TwoFactorSetupResponse(BaseModel):
    """Two-factor setup response"""
    setup_token: str
    qr_code_url: Optional[str] = None
    backup_codes: List[str] = []
    method: str


class TwoFactorVerifyRequest(BaseModel):
    """Two-factor verification request"""
    code: str = Field(..., min_length=6, max_length=6)
    setup_token: str


class TwoFactorDisableRequest(BaseModel):
    """Two-factor disable request"""
    password: str
    method: Optional[str] = None


# ==================== NOTIFICATION PREFERENCES ====================

class NotificationPreferencesUpdate(BaseModel):
    """Update notification preferences"""
    sms_enabled: Optional[bool] = None
    email_enabled: Optional[bool] = None
    push_enabled: Optional[bool] = None
    in_app_enabled: Optional[bool] = None
    emergency_alerts: Optional[bool] = None
    incident_updates: Optional[bool] = None
    geofence_alerts: Optional[bool] = None
    marketing_emails: Optional[bool] = None


class NotificationPreferencesResponse(BaseModel):
    """Notification preferences response"""
    sms_enabled: bool
    email_enabled: bool
    push_enabled: bool
    in_app_enabled: bool
    emergency_alerts: bool
    incident_updates: bool
    geofence_alerts: bool
    marketing_emails: bool


# ==================== SESSION ====================

class SessionResponse(BaseModel):
    """User session response"""
    session_id: str
    device_name: Optional[str] = None
    device_type: str
    last_activity: datetime
    ip_address: str
    user_agent: str
    is_current: bool = False


class LogoutRequest(BaseModel):
    """Logout request"""
    all_devices: bool = False
    session_id: Optional[str] = None
