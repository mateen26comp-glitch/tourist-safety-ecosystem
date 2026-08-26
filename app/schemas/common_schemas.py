"""
Pydantic schemas for request/response validation.
Common schemas used across multiple endpoints.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, validator
import enum


class UserRole(str, enum.Enum):
    """User roles"""
    TOURIST = "tourist"
    HOTEL = "hotel"
    TOUR_OPERATOR = "tour_operator"
    POLICE = "police"
    HOSPITAL = "hospital"
    TOURISM_AUTHORITY = "tourism_authority"
    ADMIN = "admin"


# ==================== PAGINATION ====================

class PaginationParams(BaseModel):
    """Pagination parameters for list endpoints"""
    skip: int = Field(0, ge=0)
    limit: int = Field(20, ge=1, le=100)
    
    class Config:
        schema_extra = {
            "example": {
                "skip": 0,
                "limit": 20
            }
        }


class PaginatedResponse(BaseModel):
    """Generic paginated response wrapper"""
    total: int
    skip: int
    limit: int
    items: List[Any]
    
    class Config:
        schema_extra = {
            "example": {
                "total": 100,
                "skip": 0,
                "limit": 20,
                "items": []
            }
        }


# ==================== ERROR RESPONSES ====================

class ErrorResponse(BaseModel):
    """Standard error response"""
    status: str = "error"
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        schema_extra = {
            "example": {
                "status": "error",
                "code": "INVALID_REQUEST",
                "message": "Invalid request parameters",
                "details": {"field": "Invalid value"},
                "timestamp": "2026-08-26T10:30:00"
            }
        }


class SuccessResponse(BaseModel):
    """Standard success response"""
    status: str = "success"
    message: str
    data: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "message": "Operation completed successfully",
                "data": {},
                "timestamp": "2026-08-26T10:30:00"
            }
        }


# ==================== LOCATION ====================

class LocationBase(BaseModel):
    """Base location schema"""
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    accuracy_meters: Optional[float] = None
    altitude_meters: Optional[float] = None
    address: Optional[str] = None
    zone_name: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "latitude": 40.7128,
                "longitude": -74.0060,
                "accuracy_meters": 10.5,
                "address": "New York, USA"
            }
        }


class LocationCreate(LocationBase):
    """Create location"""
    device_id: Optional[str] = None
    device_type: Optional[str] = None


class LocationResponse(LocationBase):
    """Location response"""
    id: int
    user_id: int
    is_real_time: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ==================== COORDINATES ====================

class CoordinateBase(BaseModel):
    """Base coordinate schema"""
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


class CoordinateDistance(CoordinateBase):
    """Coordinate with distance"""
    distance_km: float


# ==================== PAGINATION & FILTERING ====================

class DateRangeFilter(BaseModel):
    """Date range filter"""
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    
    class Config:
        schema_extra = {
            "example": {
                "start_date": "2026-08-01T00:00:00",
                "end_date": "2026-08-31T23:59:59"
            }
        }


class SortParams(BaseModel):
    """Sorting parameters"""
    sort_by: str = "created_at"
    sort_order: str = Field("desc", pattern="^(asc|desc)$")
    
    class Config:
        schema_extra = {
            "example": {
                "sort_by": "created_at",
                "sort_order": "desc"
            }
        }


# ==================== HEALTH CHECK ====================

class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    timestamp: datetime
    database: str = "connected"
    services: Dict[str, str] = {}
    
    class Config:
        schema_extra = {
            "example": {
                "status": "healthy",
                "version": "1.0.0",
                "timestamp": "2026-08-26T10:30:00",
                "database": "connected",
                "services": {
                    "notifications": "available",
                    "geofencing": "available"
                }
            }
        }


# ==================== TOKEN ====================

class TokenResponse(BaseModel):
    """Token response"""
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    expires_in: int
    
    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJhbGc...",
                "refresh_token": "eyJhbGc...",
                "token_type": "bearer",
                "expires_in": 1800
            }
        }


class TokenRefreshRequest(BaseModel):
    """Refresh token request"""
    refresh_token: str
    
    class Config:
        schema_extra = {
            "example": {
                "refresh_token": "eyJhbGc..."
            }
        }


# ==================== FILE UPLOAD ====================

class FileUploadResponse(BaseModel):
    """File upload response"""
    file_id: str
    file_name: str
    file_url: str
    file_size_mb: float
    upload_timestamp: datetime
    
    class Config:
        schema_extra = {
            "example": {
                "file_id": "file_123",
                "file_name": "incident_photo.jpg",
                "file_url": "https://example.com/files/incident_photo.jpg",
                "file_size_mb": 2.5,
                "upload_timestamp": "2026-08-26T10:30:00"
            }
        }


# ==================== NOTIFICATION ====================

class NotificationPreferences(BaseModel):
    """User notification preferences"""
    sms_enabled: bool = True
    email_enabled: bool = True
    push_enabled: bool = True
    in_app_enabled: bool = True
    emergency_alerts: bool = True
    incident_updates: bool = True
    geofence_alerts: bool = True
    marketing_emails: bool = False


class Notification(BaseModel):
    """Notification schema"""
    id: str
    user_id: int
    title: str
    message: str
    type: str  # emergency, incident, alert, info
    read: bool = False
    created_at: datetime
    
    class Config:
        from_attributes = True


# ==================== PHONE NUMBER ====================

class PhoneNumber(BaseModel):
    """Phone number with country code"""
    country_code: str = Field(..., pattern=r"^\+\d{1,3}$")
    number: str = Field(..., pattern=r"^\d{6,15}$")
    
    @property
    def full_number(self) -> str:
        """Get full phone number"""
        return f"{self.country_code}{self.number}"
    
    class Config:
        schema_extra = {
            "example": {
                "country_code": "+1",
                "number": "5551234567"
            }
        }


# ==================== METADATA ====================

class TimestampMixin(BaseModel):
    """Timestamp mixin"""
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class AuditInfo(BaseModel):
    """Audit information"""
    created_by: Optional[int] = None
    created_at: datetime
    updated_by: Optional[int] = None
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ==================== STATISTICS ====================

class StatisticValue(BaseModel):
    """Single statistic value"""
    label: str
    value: Any
    change_percent: Optional[float] = None
    trend: Optional[str] = None  # up, down, stable


class StatisticsResponse(BaseModel):
    """Statistics response"""
    period: str  # day, week, month
    statistics: List[StatisticValue]
    generated_at: datetime
    
    class Config:
        schema_extra = {
            "example": {
                "period": "day",
                "statistics": [
                    {"label": "Total Incidents", "value": 42, "change_percent": 5.2, "trend": "up"}
                ],
                "generated_at": "2026-08-26T10:30:00"
            }
        }


# ==================== COORDINATES & DISTANCE ====================

class GeoPoint(BaseModel):
    """Geographic point"""
    latitude: float
    longitude: float
    name: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "latitude": 40.7128,
                "longitude": -74.0060,
                "name": "New York"
            }
        }


class Distance(BaseModel):
    """Distance between two points"""
    from_point: GeoPoint
    to_point: GeoPoint
    distance_km: float
    distance_miles: float
    
    class Config:
        schema_extra = {
            "example": {
                "from_point": {"latitude": 40.7128, "longitude": -74.0060},
                "to_point": {"latitude": 34.0522, "longitude": -118.2437},
                "distance_km": 3944.5,
                "distance_miles": 2451.2
            }
        }
