"""
Pydantic schemas for SOS Emergency and Tourist Group Coordination endpoints.
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, validator
from app.schemas.common_schemas import TimestampMixin


# ==================== SOS STATUS & PRIORITY ====================

class SOSStatusEnum(str):
    """SOS statuses"""
    TRIGGERED = "triggered"
    ACKNOWLEDGED = "acknowledged"
    DISPATCHED = "dispatched"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CANCELLED = "cancelled"


class SOSPriorityEnum(str):
    """SOS priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class EmergencyServiceTypeEnum(str):
    """Emergency service types"""
    POLICE = "police"
    AMBULANCE = "ambulance"
    FIRE = "fire"
    HOSPITAL = "hospital"
    EMBASSY = "embassy"
    HELPLINE = "helpline"
    ALL = "all"


# ==================== SOS CREATION & UPDATE ====================

class SOSCreateRequest(BaseModel):
    """Create SOS request"""
    reason: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = "critical"
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    altitude: Optional[float] = None
    accuracy_meters: Optional[float] = None
    address: Optional[str] = None
    services_requested: Optional[List[str]] = None
    
    class Config:
        schema_extra = {
            "example": {
                "reason": "Under attack",
                "description": "Being attacked in the street",
                "priority": "critical",
                "latitude": 40.7128,
                "longitude": -74.0060,
                "address": "Times Square, NYC",
                "services_requested": ["police", "ambulance"]
            }
        }


class SOSUpdateRequest(BaseModel):
    """Update SOS request"""
    status: Optional[str] = None
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address: Optional[str] = None
    services_dispatched: Optional[bool] = None


class SOSAcknowledgeRequest(BaseModel):
    """Acknowledge SOS"""
    acknowledged_by_id: int
    response_notes: Optional[str] = None
    estimated_arrival_minutes: Optional[int] = None


class SOSResolveRequest(BaseModel):
    """Resolve SOS"""
    resolution_notes: str
    assistance_provided: bool
    user_satisfaction: Optional[int] = Field(None, ge=1, le=5)
    feedback: Optional[str] = None


# ==================== SOS RESPONSES ====================

class SOSUpdateRecord(BaseModel):
    """SOS update record"""
    id: int
    update_type: str
    update_message: str
    old_status: Optional[str]
    new_status: Optional[str]
    updated_by_id: Optional[int]
    update_source: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class SOSResponse(TimestampMixin):
    """SOS response"""
    id: int
    sos_id: str
    user_id: int
    user_name: str
    user_phone: str
    reason: Optional[str]
    description: Optional[str]
    priority: str
    status: str
    latitude: float
    longitude: float
    altitude: Optional[float]
    accuracy_meters: Optional[float]
    address: Optional[str]
    services_requested: Optional[str]
    services_notified: bool
    services_dispatched: bool
    dispatch_time: Optional[datetime]
    emergency_contacts_notified: bool
    emergency_contacts_notified_at: Optional[datetime]
    responded_by_id: Optional[int]
    responded_at: Optional[datetime]
    response_notes: Optional[str]
    estimated_arrival_minutes: Optional[int]
    resolved_at: Optional[datetime]
    resolution_notes: Optional[str]
    assistance_provided: bool
    user_satisfaction: Optional[int]
    feedback: Optional[str]
    triggered_at: datetime
    updates: List[SOSUpdateRecord] = []
    
    class Config:
        from_attributes = True


class SOSListResponse(BaseModel):
    """SOS list response"""
    id: int
    sos_id: str
    user_name: str
    reason: Optional[str]
    priority: str
    status: str
    address: Optional[str]
    triggered_at: datetime
    resolved_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class SOSStatistics(BaseModel):
    """SOS statistics"""
    total_sos: int
    active_sos: int
    resolved_sos: int
    average_response_time_minutes: Optional[float]
    sos_by_priority: dict
    sos_by_service: dict
    assisted_count: int
    satisfaction_rating: Optional[float]
    
    class Config:
        schema_extra = {
            "example": {
                "total_sos": 50,
                "active_sos": 5,
                "resolved_sos": 45,
                "average_response_time_minutes": 8.5,
                "sos_by_priority": {
                    "critical": 20,
                    "high": 15,
                    "medium": 10,
                    "low": 5
                },
                "sos_by_service": {
                    "police": 25,
                    "ambulance": 15,
                    "fire": 5
                },
                "assisted_count": 40,
                "satisfaction_rating": 4.2
            }
        }


# ==================== TOURIST GROUP ====================

class TouristGroupBase(BaseModel):
    """Base tourist group"""
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    destination: Optional[str] = None
    travel_start_date: Optional[datetime] = None
    travel_end_date: Optional[datetime] = None
    max_members: Optional[int] = None


class TouristGroupCreate(TouristGroupBase):
    """Create tourist group"""
    share_location: bool = True
    share_check_in: bool = True
    enable_group_sos: bool = True
    enable_panic_alert: bool = True
    location_update_interval_seconds: int = 60


class TouristGroupUpdate(BaseModel):
    """Update tourist group"""
    name: Optional[str] = None
    description: Optional[str] = None
    destination: Optional[str] = None
    travel_start_date: Optional[datetime] = None
    travel_end_date: Optional[datetime] = None
    share_location: Optional[bool] = None
    share_check_in: Optional[bool] = None
    enable_group_sos: Optional[bool] = None
    enable_panic_alert: Optional[bool] = None
    location_update_interval_seconds: Optional[int] = None


class TouristGroupResponse(TouristGroupBase, TimestampMixin):
    """Tourist group response"""
    id: int
    group_id: str
    created_by_id: int
    total_members: int
    join_code: str
    share_location: bool
    share_check_in: bool
    enable_group_sos: bool
    enable_panic_alert: bool
    location_update_interval_seconds: int
    is_active: bool
    status: str
    last_location_update: Optional[datetime]
    
    class Config:
        from_attributes = True


# ==================== GROUP MEMBER ====================

class GroupMemberBase(BaseModel):
    """Base group member"""
    is_admin: bool = False
    is_leader: bool = False
    can_share_location: bool = True
    can_send_alerts: bool = True
    can_manage_members: bool = False


class GroupMemberCreate(GroupMemberBase):
    """Create group member"""
    user_id: int


class GroupMemberUpdate(BaseModel):
    """Update group member"""
    is_admin: Optional[bool] = None
    is_leader: Optional[bool] = None
    can_share_location: Optional[bool] = None
    can_send_alerts: Optional[bool] = None
    can_manage_members: Optional[bool] = None


class GroupMemberResponse(GroupMemberBase, TimestampMixin):
    """Group member response"""
    id: int
    group_id: int
    user_id: int
    user_name: str
    user_email: str
    join_status: str
    joined_at: datetime
    left_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class GroupMemberListResponse(BaseModel):
    """Group members list response"""
    total_members: int
    members: List[GroupMemberResponse]


# ==================== GROUP LOCATION ====================

class GroupLocationResponse(BaseModel):
    """Group member location"""
    id: int
    group_id: int
    user_id: int
    user_name: str
    latitude: float
    longitude: float
    accuracy_meters: Optional[float]
    address: Optional[str]
    is_latest: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class GroupLocationsResponse(BaseModel):
    """All group member locations"""
    group_id: int
    total_members: int
    locations: List[GroupLocationResponse]
    last_update: datetime


# ==================== GROUP PANIC ALERT ====================

class GroupPanicAlertCreateRequest(BaseModel):
    """Create group panic alert"""
    reason: Optional[str] = None
    severity: str = "high"
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    address: Optional[str] = None


class GroupPanicAlertResponse(TimestampMixin):
    """Group panic alert response"""
    id: int
    alert_id: str
    group_id: int
    triggered_by_id: int
    triggered_by_name: str
    reason: Optional[str]
    severity: str
    alert_latitude: float
    alert_longitude: float
    alert_address: Optional[str]
    members_notified_count: int
    members_acknowledged_count: int
    emergency_services_called: bool
    resolved: bool
    resolved_at: Optional[datetime]
    resolution_notes: Optional[str]
    
    class Config:
        from_attributes = True


# ==================== GROUP CHECK-IN ====================

class CheckInStatus(str):
    """Check-in statuses"""
    SAFE = "safe"
    NEED_HELP = "need_help"
    EMERGENCY = "emergency"


class GroupCheckInCreateRequest(BaseModel):
    """Create group check-in"""
    status: str = Field(..., pattern="^(safe|need_help|emergency)$")
    message: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address: Optional[str] = None


class GroupCheckInResponse(TimestampMixin):
    """Group check-in response"""
    id: int
    group_id: int
    user_id: int
    user_name: str
    status: str
    message: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    address: Optional[str]
    
    class Config:
        from_attributes = True


class GroupCheckInStatusResponse(BaseModel):
    """Group check-in status response"""
    group_id: int
    total_members: int
    safe_count: int
    need_help_count: int
    emergency_count: int
    check_ins: List[GroupCheckInResponse]


# ==================== GROUP JOIN & LEAVE ====================

class JoinGroupRequest(BaseModel):
    """Join group request"""
    join_code: str = Field(..., min_length=6, max_length=20)


class JoinGroupResponse(BaseModel):
    """Join group response"""
    message: str
    group: TouristGroupResponse
    member: GroupMemberResponse


class LeaveGroupRequest(BaseModel):
    """Leave group request"""
    reason: Optional[str] = None


class RemoveGroupMemberRequest(BaseModel):
    """Remove member from group"""
    user_id: int
    reason: Optional[str] = None


# ==================== GROUP STATISTICS ====================

class GroupStatistics(BaseModel):
    """Group statistics"""
    total_groups: int
    active_groups: int
    total_members: int
    average_group_size: float
    panic_alerts_triggered: int
    emergency_calls: int
    check_ins_last_24h: int
    
    class Config:
        schema_extra = {
            "example": {
                "total_groups": 25,
                "active_groups": 18,
                "total_members": 250,
                "average_group_size": 10.0,
                "panic_alerts_triggered": 5,
                "emergency_calls": 2,
                "check_ins_last_24h": 180
            }
        }


# ==================== GROUP ACTIVITY ====================

class GroupActivityLog(BaseModel):
    """Group activity log entry"""
    id: int
    group_id: int
    activity_type: str
    description: str
    user_id: Optional[int]
    user_name: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class GroupActivityResponse(BaseModel):
    """Group activity response"""
    group_id: int
    total_activities: int
    activities: List[GroupActivityLog]
