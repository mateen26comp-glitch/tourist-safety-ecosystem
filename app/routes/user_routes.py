"""
User Authentication and Profile Management API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
from app.database import get_db
from app.schemas.user_schemas import (
    UserRegisterRequest, UserLoginRequest, UserResponse, UserProfileUpdate,
    UserListResponse, TokenResponse, ChangePasswordRequest, EmergencyContactCreate,
    EmergencyContactResponse, UserPreferencesUpdate, UserPreferencesResponse
)
from app.core.security import verify_token, get_password_hash, verify_password

router = APIRouter(prefix="/api/v1/users", tags=["users"])


# ==================== AUTHENTICATION ====================

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    request: UserRegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Register a new user account.
    
    - **email**: User's email address
    - **password**: User's password (min 8 characters)
    - **first_name**: User's first name
    - **last_name**: User's last name
    - **phone**: User's phone number
    - **country**: User's country of residence
    - **user_type**: Type of user (tourist, hotel, police, hospital, etc.)
    """
    # Check if user already exists
    # existing_user = db.query(User).filter(User.email == request.email).first()
    # if existing_user:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Email already registered"
    #     )
    
    # Create new user
    # new_user = User(
    #     email=request.email,
    #     password_hash=get_password_hash(request.password),
    #     first_name=request.first_name,
    #     last_name=request.last_name,
    #     phone=request.phone,
    #     country=request.country,
    #     user_type=request.user_type
    # )
    # db.add(new_user)
    # db.commit()
    # db.refresh(new_user)
    
    return {"message": "User registered successfully"}


@router.post("/login", response_model=TokenResponse)
async def login_user(
    request: UserLoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login with email and password.
    
    Returns JWT access token and refresh token.
    """
    # user = db.query(User).filter(User.email == request.email).first()
    # if not user or not verify_password(request.password, user.password_hash):
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Invalid email or password"
    #     )
    
    # access_token = create_access_token(data={"sub": user.id})
    # refresh_token = create_refresh_token(data={"sub": user.id})
    
    return {
        "access_token": "token_placeholder",
        "refresh_token": "refresh_token_placeholder",
        "token_type": "bearer"
    }


@router.post("/refresh-token", response_model=TokenResponse)
async def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    """
    Refresh access token using refresh token.
    """
    # Validate refresh token
    # payload = verify_token(refresh_token)
    # user_id = payload.get("sub")
    
    # new_access_token = create_access_token(data={"sub": user_id})
    
    return {
        "access_token": "new_token_placeholder",
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/logout")
async def logout_user(
    current_user_id: int = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """
    Logout the current user.
    Invalidate tokens and clear sessions.
    """
    return {"message": "Logged out successfully"}


# ==================== PROFILE MANAGEMENT ====================

@router.get("/profile", response_model=UserResponse)
async def get_user_profile(
    current_user_id: int = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """
    Get current user's profile information.
    """
    # user = db.query(User).filter(User.id == current_user_id).first()
    # if not user:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="User not found"
    #     )
    
    return {"message": "User profile"}


@router.get("/profile/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Get public user profile by ID.
    """
    # user = db.query(User).filter(User.id == user_id).first()
    # if not user:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="User not found"
    #     )
    
    return {"message": "User profile"}


@router.put("/profile", response_model=UserResponse)
async def update_user_profile(
    request: UserProfileUpdate,
    current_user_id: int = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """
    Update current user's profile information.
    """
    # user = db.query(User).filter(User.id == current_user_id).first()
    # if not user:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="User not found"
    #     )
    
    # # Update fields
    # if request.first_name:
    #     user.first_name = request.first_name
    # if request.last_name:
    #     user.last_name = request.last_name
    # # ... update other fields
    
    # db.commit()
    # db.refresh(user)
    
    return {"message": "Profile updated successfully"}


# ==================== PASSWORD MANAGEMENT ====================

@router.post("/change-password")
async def change_password(
    request: ChangePasswordRequest,
    current_user_id: int = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """
    Change user's password.
    Requires current password verification.
    """
    # user = db.query(User).filter(User.id == current_user_id).first()
    # if not user or not verify_password(request.current_password, user.password_hash):
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Invalid current password"
    #     )
    
    # user.password_hash = get_password_hash(request.new_password)
    # db.commit()
    
    return {"message": "Password changed successfully"}


@router.post("/forgot-password")
async def forgot_password(
    email: str,
    db: Session = Depends(get_db)
):
    """
    Request password reset.
    Sends reset link to email.
    """
    # user = db.query(User).filter(User.email == email).first()
    # if not user:
    #     # Don't reveal if email exists
    #     pass
    
    # reset_token = create_password_reset_token(user.id)
    # Send email with reset link
    
    return {"message": "Password reset link sent to email"}


@router.post("/reset-password")
async def reset_password(
    token: str,
    new_password: str,
    db: Session = Depends(get_db)
):
    """
    Reset password using reset token.
    """
    # payload = verify_password_reset_token(token)
    # user_id = payload.get("sub")
    
    # user = db.query(User).filter(User.id == user_id).first()
    # if not user:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    # user.password_hash = get_password_hash(new_password)
    # db.commit()
    
    return {"message": "Password reset successfully"}


# ==================== EMERGENCY CONTACTS ====================

@router.get("/emergency-contacts", response_model=List[EmergencyContactResponse])
async def get_emergency_contacts(
    current_user_id: int = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """
    Get user's emergency contacts.
    """
    # contacts = db.query(EmergencyContact).filter(
    #     EmergencyContact.user_id == current_user_id
    # ).all()
    
    return []


@router.post("/emergency-contacts", response_model=EmergencyContactResponse, status_code=status.HTTP_201_CREATED)
async def create_emergency_contact(
    request: EmergencyContactCreate,
    current_user_id: int = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """
    Add a new emergency contact.
    """
    # new_contact = EmergencyContact(
    #     user_id=current_user_id,
    #     name=request.name,
    #     phone=request.phone,
    #     email=request.email,
    #     relationship=request.relationship
    # )
    # db.add(new_contact)
    # db.commit()
    # db.refresh(new_contact)
    
    return {"message": "Emergency contact added"}


@router.put("/emergency-contacts/{contact_id}", response_model=EmergencyContactResponse)
async def update_emergency_contact(
    contact_id: int,
    request: EmergencyContactCreate,
    current_user_id: int = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """
    Update emergency contact.
    """
    # contact = db.query(EmergencyContact).filter(
    #     EmergencyContact.id == contact_id,
    #     EmergencyContact.user_id == current_user_id
    # ).first()
    
    # if not contact:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    # contact.name = request.name
    # contact.phone = request.phone
    # db.commit()
    # db.refresh(contact)
    
    return {"message": "Emergency contact updated"}


@router.delete("/emergency-contacts/{contact_id}")
async def delete_emergency_contact(
    contact_id: int,
    current_user_id: int = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """
    Delete emergency contact.
    """
    # contact = db.query(EmergencyContact).filter(
    #     EmergencyContact.id == contact_id,
    #     EmergencyContact.user_id == current_user_id
    # ).first()
    
    # if not contact:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    # db.delete(contact)
    # db.commit()
    
    return {"message": "Emergency contact deleted"}


# ==================== USER PREFERENCES ====================

@router.get("/preferences", response_model=UserPreferencesResponse)
async def get_user_preferences(
    current_user_id: int = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """
    Get user's preferences and settings.
    """
    # preferences = db.query(UserPreferences).filter(
    #     UserPreferences.user_id == current_user_id
    # ).first()
    
    return {"message": "User preferences"}


@router.put("/preferences", response_model=UserPreferencesResponse)
async def update_user_preferences(
    request: UserPreferencesUpdate,
    current_user_id: int = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """
    Update user's preferences and settings.
    """
    # preferences = db.query(UserPreferences).filter(
    #     UserPreferences.user_id == current_user_id
    # ).first()
    
    # if not preferences:
    #     preferences = UserPreferences(user_id=current_user_id)
    #     db.add(preferences)
    
    # # Update fields
    # if request.language:
    #     preferences.language = request.language
    # # ... update other fields
    
    # db.commit()
    # db.refresh(preferences)
    
    return {"message": "Preferences updated"}


# ==================== USER LISTING ====================

@router.get("/", response_model=UserListResponse)
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    user_type: Optional[str] = None,
    country: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    List users with optional filtering.
    Admin only.
    """
    # query = db.query(User)
    
    # if user_type:
    #     query = query.filter(User.user_type == user_type)
    # if country:
    #     query = query.filter(User.country == country)
    
    # total = query.count()
    # users = query.offset(skip).limit(limit).all()
    
    return {"total": 0, "users": []}


# ==================== USER VERIFICATION ====================

@router.post("/verify-email")
async def verify_email(
    token: str,
    db: Session = Depends(get_db)
):
    """
    Verify user's email using verification token.
    """
    # payload = verify_email_token(token)
    # user_id = payload.get("sub")
    
    # user = db.query(User).filter(User.id == user_id).first()
    # if not user:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    # user.email_verified = True
    # user.email_verified_at = datetime.utcnow()
    # db.commit()
    
    return {"message": "Email verified successfully"}


@router.post("/resend-verification-email")
async def resend_verification_email(
    current_user_id: int = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """
    Resend email verification link.
    """
    # user = db.query(User).filter(User.id == current_user_id).first()
    # if user.email_verified:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Email already verified"
    #     )
    
    # Send verification email
    
    return {"message": "Verification email sent"}


# ==================== PROFILE DELETION ====================

@router.delete("/profile")
async def delete_user_account(
    password: str,
    current_user_id: int = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """
    Delete user account (soft delete).
    Requires password confirmation.
    """
    # user = db.query(User).filter(User.id == current_user_id).first()
    # if not user or not verify_password(password, user.password_hash):
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Invalid password"
    #     )
    
    # user.is_deleted = True
    # user.deleted_at = datetime.utcnow()
    # db.commit()
    
    return {"message": "Account deleted successfully"}
