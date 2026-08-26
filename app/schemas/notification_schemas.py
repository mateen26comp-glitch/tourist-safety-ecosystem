"""
Pydantic schemas for Notification endpoints.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from app.schemas.common_schemas import TimestampMixin


# ==================== NOTIFICATION TYPES ====================

class NotificationTypeEnum(str):
    """Notification types"""
    EMERGENCY_ALERT = "emergency_alert"
    INCIDENT_UPDATE = "incident_update"
    SOS_RESPONSE = "sos_response"
    GEOFENCE_ALERT = "geofence_alert"
    GROUP_ALERT = "group_alert"
    CHECK_IN_REMINDER = "check_in_reminder"
    SAFETY_TIP = "safety_tip"
    INCIDENT_RESOLVED = "incident_resolved"
    OFFICIAL_ANNOUNCEMENT = "official_announcement"
    SYSTEM_NOTIFICATION = "system_notification"


class NotificationChannelEnum(str):
    """Notification channels"""
    SMS = "sms"
    EMAIL = "email"
    PUSH = "push"
    IN_APP = "in_app"
    VOICE_CALL = "voice_call"


class NotificationPriorityEnum(str):
    """Notification priority levels"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


# ==================== NOTIFICATION CREATION ====================

class NotificationCreate(BaseModel):
    """Create notification"""
    user_id: int
    title: str = Field(..., max_length=255)
    message: str = Field(..., min_length=1)
    notification_type: str
    priority: str = "normal"
    channels: Optional[List[str]] = None  # sms, email, push, in_app
    related_to_id: Optional[int] = None
    related_to_type: Optional[str] = None
    action_url: Optional[str] = None
    icon_url: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "user_id": 1,
                "title": "Emergency Alert",
                "message": "There is an active incident near you",
                "notification_type": "emergency_alert",
                "priority": "critical",
                "channels": ["push", "sms"],
                "related_to_id": 10,
                "related_to_type": "incident"
            }
        }


class BulkNotificationCreate(BaseModel):
    """Create bulk notification"""
    user_ids: List[int]
    title: str = Field(..., max_length=255)
    message: str = Field(..., min_length=1)
    notification_type: str
    priority: str = "normal"
    channels: Optional[List[str]] = None
    action_url: Optional[str] = None
    send_immediately: bool = True


class ScheduledNotificationCreate(BaseModel):
    """Create scheduled notification"""
    user_id: int
    title: str = Field(..., max_length=255)
    message: str = Field(..., min_length=1)
    notification_type: str
    priority: str = "normal"
    channels: Optional[List[str]] = None
    scheduled_at: datetime
    repeat_pattern: Optional[str] = None  # daily, weekly, monthly
    repeat_until: Optional[datetime] = None


# ==================== NOTIFICATION RESPONSES ====================

class NotificationResponse(TimestampMixin):
    """Notification response"""
    id: int
    user_id: int
    title: str
    message: str
    notification_type: str
    priority: str
    read: bool
    read_at: Optional[datetime]
    action_url: Optional[str]
    icon_url: Optional[str]
    related_to_id: Optional[int]
    related_to_type: Optional[str]
    
    class Config:
        from_attributes = True


class NotificationDetailResponse(NotificationResponse):
    """Detailed notification response"""
    delivery_channels: List[str]
    delivery_status: Dict[str, str]  # channel -> status
    delivered_at: Optional[datetime]
    failed_reason: Optional[str]


class NotificationListResponse(BaseModel):
    """Notification list response"""
    total: int
    unread_count: int
    notifications: List[NotificationResponse]


# ==================== NOTIFICATION ACTIONS ====================

class NotificationMarkAsRead(BaseModel):
    """Mark notification as read"""
    notification_id: Optional[int] = None
    all: bool = False


class NotificationMarkAsUnread(BaseModel):
    """Mark notification as unread"""
    notification_id: int


class NotificationDelete(BaseModel):
    """Delete notification"""
    notification_id: Optional[int] = None
    older_than_days: Optional[int] = None
    all: bool = False


class NotificationArchive(BaseModel):
    """Archive notification"""
    notification_id: Optional[int] = None
    all: bool = False


# ==================== NOTIFICATION DELIVERY ====================

class NotificationDeliveryLog(BaseModel):
    """Notification delivery log"""
    id: int
    notification_id: int
    channel: str
    status: str  # sent, failed, delivered, read
    sent_at: datetime
    delivered_at: Optional[datetime]
    error_message: Optional[str]
    retry_count: int


class NotificationDeliveryRequest(BaseModel):
    """Notification delivery request"""
    notification_ids: List[int]
    channels: Optional[List[str]] = None
    force_send: bool = False


class NotificationDeliveryResponse(BaseModel):
    """Notification delivery response"""
    total: int
    successful: int
    failed: int
    delivery_logs: List[NotificationDeliveryLog]


# ==================== NOTIFICATION PREFERENCES ====================

class NotificationChannelPreference(BaseModel):
    """Notification channel preference"""
    channel: str
    enabled: bool
    quiet_hours_start: Optional[str] = None  # HH:MM format
    quiet_hours_end: Optional[str] = None
    delivery_time: Optional[str] = None


class NotificationTypePreference(BaseModel):
    """Notification type preference"""
    notification_type: str
    enabled: bool
    priority_threshold: Optional[str] = None  # min priority to receive
    channels: Optional[List[str]] = None


class NotificationPreferencesUpdate(BaseModel):
    """Update notification preferences"""
    channel_preferences: Optional[List[NotificationChannelPreference]] = None
    type_preferences: Optional[List[NotificationTypePreference]] = None
    do_not_disturb_enabled: Optional[bool] = None
    do_not_disturb_start: Optional[str] = None
    do_not_disturb_end: Optional[str] = None
    critical_alerts_override_dnd: Optional[bool] = None


class NotificationPreferencesResponse(BaseModel):
    """Notification preferences response"""
    user_id: int
    channel_preferences: List[NotificationChannelPreference]
    type_preferences: List[NotificationTypePreference]
    do_not_disturb_enabled: bool
    do_not_disturb_start: Optional[str]
    do_not_disturb_end: Optional[str]
    critical_alerts_override_dnd: bool
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ==================== NOTIFICATION TEMPLATES ====================

class NotificationTemplate(BaseModel):
    """Notification template"""
    id: int
    name: str
    description: Optional[str]
    notification_type: str
    title_template: str
    message_template: str
    default_channels: List[str]
    default_priority: str
    created_at: datetime


class NotificationTemplateCreate(BaseModel):
    """Create notification template"""
    name: str
    description: Optional[str]
    notification_type: str
    title_template: str
    message_template: str
    default_channels: List[str]
    default_priority: str = "normal"


class SendWithTemplateRequest(BaseModel):
    """Send notification using template"""
    template_id: int
    user_id: int
    template_variables: Optional[Dict[str, Any]] = None


# ==================== NOTIFICATION ANALYTICS ====================

class NotificationStats(BaseModel):
    """Notification statistics"""
    total_sent: int
    total_delivered: int
    total_read: int
    total_failed: int
    delivery_rate: float
    read_rate: float
    by_type: Dict[str, int]
    by_channel: Dict[str, int]
    by_priority: Dict[str, int]
    average_delivery_time_seconds: Optional[float]
    
    class Config:
        schema_extra = {
            "example": {
                "total_sent": 1000,
                "total_delivered": 950,
                "total_read": 800,
                "total_failed": 50,
                "delivery_rate": 95.0,
                "read_rate": 80.0,
                "by_type": {
                    "emergency_alert": 100,
                    "incident_update": 500
                },
                "by_channel": {
                    "push": 600,
                    "sms": 300,
                    "email": 100
                },
                "by_priority": {
                    "critical": 100,
                    "high": 200
                },
                "average_delivery_time_seconds": 2.5
            }
        }


class NotificationStatsRequest(BaseModel):
    """Notification stats request"""
    user_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    notification_type: Optional[str] = None
    channel: Optional[str] = None


# ==================== NOTIFICATION BATCH ====================

class NotificationBatch(BaseModel):
    """Notification batch"""
    id: str
    total_notifications: int
    sent_count: int
    delivered_count: int
    failed_count: int
    status: str
    created_at: datetime
    completed_at: Optional[datetime]


class NotificationBatchResponse(BaseModel):
    """Notification batch response"""
    batch_id: str
    message: str
    status: str
    notifications: List[NotificationResponse]


# ==================== NOTIFICATION EVENTS ====================

class NotificationEventLog(BaseModel):
    """Notification event log"""
    id: int
    notification_id: int
    event_type: str  # sent, delivered, read, failed
    event_timestamp: datetime
    user_agent: Optional[str]
    ip_address: Optional[str]
    additional_data: Optional[Dict[str, Any]]
    
    class Config:
        from_attributes = True


class NotificationEventStatsResponse(BaseModel):
    """Notification event statistics"""
    notification_id: int
    total_events: int
    events: List[NotificationEventLog]
