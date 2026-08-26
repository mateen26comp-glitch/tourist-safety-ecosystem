"""
Database models for User, Profile, and Authentication.
Defines the structure for users with multiple roles and their profiles.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()


class UserRole(str, enum.Enum):
    """Enum for user roles in the system"""
    TOURIST = "tourist"
    HOTEL = "hotel"
    TOUR_OPERATOR = "tour_operator"
    POLICE = "police"
    HOSPITAL = "hospital"
    TOURISM_AUTHORITY = "tourism_authority"
    ADMIN = "admin"


class User(Base):
    """
    Main User model supporting multiple roles.
    Stores authentication credentials and basic user information.
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(20), unique=True, nullable=True)
    
    # Authentication
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, index=True)
    is_verified = Column(Boolean, default=False)
    email_verified_at = Column(DateTime, nullable=True)
    phone_verified_at = Column(DateTime, nullable=True)
    
    # Role & Permissions
    role = Column(Enum(UserRole), default=UserRole.TOURIST, index=True)
    is_superuser = Column(Boolean, default=False)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    emergency_contacts = relationship("EmergencyContact", back_populates="user", cascade="all, delete-orphan")
    incidents = relationship("Incident", back_populates="reporter", foreign_keys="Incident.reporter_id")
    sos_records = relationship("SOSRecord", back_populates="user", cascade="all, delete-orphan")
    locations = relationship("UserLocation", back_populates="user", cascade="all, delete-orphan")
    group_memberships = relationship("GroupMember", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email}, role={self.role})>"


class UserProfile(Base):
    """
    Extended user profile information.
    Stores detailed profile data for tourists and service providers.
    """
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    # Personal Information
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    date_of_birth = Column(DateTime, nullable=True)
    gender = Column(String(20), nullable=True)
    nationality = Column(String(100), nullable=True)
    passport_number = Column(String(50), unique=True, nullable=True)
    
    # Contact Information
    emergency_contact_name = Column(String(100), nullable=True)
    emergency_contact_phone = Column(String(20), nullable=True)
    emergency_contact_email = Column(String(255), nullable=True)
    
    # Travel Information (for Tourists)
    current_destination = Column(String(255), nullable=True)
    travel_dates_from = Column(DateTime, nullable=True)
    travel_dates_to = Column(DateTime, nullable=True)
    accommodation_address = Column(Text, nullable=True)
    accommodation_phone = Column(String(20), nullable=True)
    
    # Medical Information
    blood_group = Column(String(10), nullable=True)
    allergies = Column(Text, nullable=True)
    medical_conditions = Column(Text, nullable=True)
    emergency_medications = Column(Text, nullable=True)
    
    # Organization Information (for Hotels, Tour Operators, etc.)
    organization_name = Column(String(255), nullable=True)
    organization_license = Column(String(100), nullable=True)
    organization_address = Column(Text, nullable=True)
    organization_website = Column(String(255), nullable=True)
    registration_number = Column(String(100), nullable=True)
    
    # Profile Status
    profile_complete = Column(Boolean, default=False)
    identity_verified = Column(Boolean, default=False)
    verification_document_url = Column(String(500), nullable=True)
    
    # Preferences
    preferred_language = Column(String(10), default="en")
    notification_preferences = Column(Text, nullable=True)  # JSON format
    two_factor_enabled = Column(Boolean, default=False)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="profile")
    
    def __repr__(self):
        return f"<UserProfile(id={self.id}, user_id={self.user_id}, name={self.first_name} {self.last_name})>"


class EmergencyContact(Base):
    """
    Stores emergency contacts for users.
    Multiple emergency contacts can be added per user.
    """
    __tablename__ = "emergency_contacts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Contact Information
    name = Column(String(100), nullable=False)
    relationship = Column(String(50), nullable=True)  # e.g., "Mother", "Brother", "Friend"
    phone = Column(String(20), nullable=False)
    email = Column(String(255), nullable=True)
    country_code = Column(String(5), default="+1")
    
    # Notification Preferences
    notify_on_sos = Column(Boolean, default=True)
    notify_on_incident = Column(Boolean, default=False)
    notify_on_geofence = Column(Boolean, default=False)
    
    # Status
    is_primary = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    verified = Column(Boolean, default=False)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="emergency_contacts")
    
    def __repr__(self):
        return f"<EmergencyContact(id={self.id}, user_id={self.user_id}, name={self.name}, phone={self.phone})>"
