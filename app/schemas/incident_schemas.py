"""
Pydantic schemas for Incident endpoints.
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, validator
from app.schemas.common_schemas import TimestampMixin, LocationBase, FileUploadResponse


# ==================== INCIDENT SEVERITY & CATEGORY ====================

class IncidentCategoryEnum(str):
    """Incident categories"""
    THEFT = "theft"
    ASSAULT = "assault"
    LOST_PERSON = "lost_person"
    MEDICAL_EMERGENCY = "medical_emergency"
    ACCIDENT = "accident"
    HARASSMENT = "harassment"
    PROPERTY_DAMAGE = "property_damage"
    SCAM = "scam"
    DOCUMENTATION_ISSUE = "documentation_issue"
    OTHER = "other"


class IncidentSeverityEnum(str):
    """Incident severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class IncidentStatusEnum(str):
    """Incident statuses"""
    REPORTED = "reported"
    ACKNOWLEDGED = "acknowledged"
    DISPATCHED = "dispatched"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"
    CANCELLED = "cancelled"


# ==================== INCIDENT CREATION & UPDATE ====================

class IncidentCreate(BaseModel):
    """Create incident request"""
    title: str = Field(..., max_length=255)
    description: str = Field(..., min_length=10)
    category: str
    severity: Optional[str] = "medium"
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    location_address: Optional[str] = None
    location_zone: Optional[str] = None
    number_of_people_affected: int = Field(default=1, ge=1)
    injuries_reported: bool = False
    property_damage_reported: bool = False
    estimated_damage_amount: Optional[float] = None
    emergency_services_type: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "title": "Theft at Market",
                "description": "Wallet stolen at the central market",
                "category": "theft",
                "severity": "high",
                "latitude": 40.7128,
                "longitude": -74.0060,
                "location_address": "Central Market, NYC",
                "number_of_people_affected": 1,
                "injuries_reported": False,
                "property_damage_reported": False
            }
        }


class IncidentUpdate(BaseModel):
    """Update incident request"""
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    severity: Optional[str] = None
    number_of_people_affected: Optional[int] = None
    injuries_reported: Optional[bool] = None
    property_damage_reported: Optional[bool] = None
    estimated_damage_amount: Optional[float] = None
    location_address: Optional[str] = None
    location_zone: Optional[str] = None


class IncidentStatusUpdate(BaseModel):
    """Update incident status"""
    status: str
    notes: Optional[str] = None
    response_notes: Optional[str] = None
    estimated_arrival_minutes: Optional[int] = None


class IncidentResolve(BaseModel):
    """Resolve incident"""
    resolution_description: str
    resolution_notes: Optional[str] = None
    user_satisfaction: Optional[int] = Field(None, ge=1, le=5)
    feedback: Optional[str] = None


# ==================== INCIDENT RESPONSES ====================

class IncidentMediaResponse(BaseModel):
    """Incident media response"""
    id: int
    file_name: str
    file_url: str
    media_type: str
    file_size_mb: Optional[float]
    duration_seconds: Optional[int]
    uploaded_at: datetime
    description: Optional[str]
    
    class Config:
        from_attributes = True


class IncidentStatusUpdateResponse(BaseModel):
    """Incident status update response"""
    id: int
    old_status: Optional[str]
    new_status: str
    update_reason: Optional[str]
    update_notes: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class IncidentCommentResponse(BaseModel):
    """Incident comment response"""
    id: int
    comment: str
    is_internal: bool
    commented_by_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class IncidentResponse(TimestampMixin):
    """Incident response"""
    id: int
    incident_id: str
    reporter_id: int
    reporter_name: str
    reporter_contact: str
    title: str
    description: str
    category: str
    severity: str
    latitude: float
    longitude: float
    location_address: Optional[str]
    location_zone: Optional[str]
    status: str
    assigned_to_id: Optional[int]
    assigned_at: Optional[datetime]
    emergency_services_notified: bool
    emergency_services_type: Optional[str]
    response_time_minutes: Optional[int]
    ai_category_prediction: Optional[str]
    ai_severity_score: Optional[float]
    ai_confidence: Optional[float]
    number_of_people_affected: int
    injuries_reported: bool
    property_damage_reported: bool
    estimated_damage_amount: Optional[float]
    resolution_description: Optional[str]
    resolved_at: Optional[datetime]
    resolution_notes: Optional[str]
    media: List[IncidentMediaResponse] = []
    status_updates: List[IncidentStatusUpdateResponse] = []
    
    class Config:
        from_attributes = True


class IncidentDetailResponse(IncidentResponse):
    """Detailed incident response"""
    comments: List[IncidentCommentResponse] = []


class IncidentListResponse(BaseModel):
    """Incident list response"""
    id: int
    incident_id: str
    title: str
    category: str
    severity: str
    status: str
    location_address: Optional[str]
    reporter_name: str
    created_at: datetime
    resolved_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# ==================== INCIDENT COMMENTS ====================

class CommentCreate(BaseModel):
    """Create incident comment"""
    comment: str = Field(..., min_length=1, max_length=1000)
    is_internal: bool = False
    
    class Config:
        schema_extra = {
            "example": {
                "comment": "Victim treated at hospital",
                "is_internal": False
            }
        }


class CommentUpdate(BaseModel):
    """Update incident comment"""
    comment: str = Field(..., min_length=1, max_length=1000)
    is_internal: Optional[bool] = None


# ==================== INCIDENT MEDIA ====================

class MediaUploadRequest(BaseModel):
    """Media upload request"""
    media_type: str = Field(..., pattern="^(image|video|audio)$")
    description: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "media_type": "image",
                "description": "Photo of stolen items"
            }
        }


class MediaResponse(BaseModel):
    """Media response"""
    id: int
    file_name: str
    file_url: str
    media_type: str
    file_size_mb: Optional[float]
    uploaded_at: datetime
    description: Optional[str]
    
    class Config:
        from_attributes = True


# ==================== INCIDENT FILTERS & SEARCH ====================

class IncidentFilterParams(BaseModel):
    """Incident filter parameters"""
    category: Optional[str] = None
    severity: Optional[str] = None
    status: Optional[str] = None
    assigned_to_id: Optional[int] = None
    reporter_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    location_zone: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    radius_km: Optional[float] = 10.0
    injuries_reported: Optional[bool] = None
    property_damage_reported: Optional[bool] = None
    
    class Config:
        schema_extra = {
            "example": {
                "category": "theft",
                "severity": "high",
                "status": "open",
                "start_date": "2026-08-01T00:00:00",
                "end_date": "2026-08-31T23:59:59"
            }
        }


class IncidentSearchRequest(BaseModel):
    """Incident search request"""
    query: str = Field(..., min_length=2)
    filters: Optional[IncidentFilterParams] = None
    skip: int = 0
    limit: int = 20


# ==================== INCIDENT ASSIGNMENT ====================

class IncidentAssignRequest(BaseModel):
    """Assign incident to staff"""
    assigned_to_id: int
    notes: Optional[str] = None


class IncidentUnassignRequest(BaseModel):
    """Unassign incident from staff"""
    notes: Optional[str] = None


# ==================== INCIDENT STATISTICS ====================

class IncidentStat(BaseModel):
    """Single incident statistic"""
    label: str
    value: int
    percentage: Optional[float] = None


class IncidentStatistics(BaseModel):
    """Incident statistics response"""
    total_incidents: int
    incidents_by_severity: List[IncidentStat]
    incidents_by_category: List[IncidentStat]
    incidents_by_status: List[IncidentStat]
    average_response_time_minutes: Optional[float]
    resolution_rate: Optional[float]
    injuries_reported_count: int
    property_damage_count: int
    critical_incidents: int
    
    class Config:
        schema_extra = {
            "example": {
                "total_incidents": 150,
                "incidents_by_severity": [
                    {"label": "Critical", "value": 10, "percentage": 6.7},
                    {"label": "High", "value": 35, "percentage": 23.3}
                ],
                "incidents_by_category": [
                    {"label": "Theft", "value": 50, "percentage": 33.3},
                    {"label": "Assault", "value": 25, "percentage": 16.7}
                ],
                "incidents_by_status": [
                    {"label": "Resolved", "value": 100, "percentage": 66.7},
                    {"label": "In Progress", "value": 30, "percentage": 20.0}
                ],
                "average_response_time_minutes": 15.5,
                "resolution_rate": 66.7,
                "injuries_reported_count": 20,
                "property_damage_count": 45,
                "critical_incidents": 10
            }
        }


# ==================== INCIDENT EXPORT ====================

class IncidentExportRequest(BaseModel):
    """Export incidents request"""
    format: str = Field(..., pattern="^(csv|pdf|json)$")
    filters: Optional[IncidentFilterParams] = None
    include_media: bool = False
    include_comments: bool = False


class IncidentExportResponse(BaseModel):
    """Export response"""
    download_url: str
    file_name: str
    file_size_mb: float
    created_at: datetime
    expires_at: datetime
