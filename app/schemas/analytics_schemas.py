"""
Pydantic schemas for Analytics and Reporting endpoints.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from app.schemas.common_schemas import TimestampMixin


# ==================== TIME PERIOD ====================

class TimePeriodEnum(str):
    """Time period options"""
    TODAY = "today"
    YESTERDAY = "yesterday"
    THIS_WEEK = "this_week"
    LAST_WEEK = "last_week"
    THIS_MONTH = "this_month"
    LAST_MONTH = "last_month"
    THIS_YEAR = "this_year"
    LAST_YEAR = "last_year"
    CUSTOM = "custom"


class ChartTypeEnum(str):
    """Chart types"""
    LINE = "line"
    BAR = "bar"
    PIE = "pie"
    DOUGHNUT = "doughnut"
    AREA = "area"
    SCATTER = "scatter"
    HEATMAP = "heatmap"


# ==================== ANALYTICS REQUESTS ====================

class AnalyticsRequest(BaseModel):
    """Analytics request"""
    metric: str
    time_period: str = "this_month"
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    group_by: Optional[str] = None  # day, week, month, zone, category, etc.
    filters: Optional[Dict[str, Any]] = None
    limit: int = 100


class CustomDateRange(BaseModel):
    """Custom date range"""
    start_date: datetime
    end_date: datetime
    
    class Config:
        schema_extra = {
            "example": {
                "start_date": "2026-08-01T00:00:00",
                "end_date": "2026-08-31T23:59:59"
            }
        }


# ==================== INCIDENT ANALYTICS ====================

class IncidentAnalytics(BaseModel):
    """Incident analytics"""
    total_incidents: int
    incidents_by_category: Dict[str, int]
    incidents_by_severity: Dict[str, int]
    incidents_by_status: Dict[str, int]
    incidents_by_zone: Dict[str, int]
    average_response_time_minutes: Optional[float]
    resolution_rate_percent: Optional[float]
    peak_incident_hours: Optional[List[int]]
    peak_incident_days: Optional[List[str]]
    
    class Config:
        schema_extra = {
            "example": {
                "total_incidents": 150,
                "incidents_by_category": {
                    "theft": 50,
                    "assault": 30,
                    "medical_emergency": 25
                },
                "incidents_by_severity": {
                    "critical": 10,
                    "high": 40,
                    "medium": 60,
                    "low": 40
                },
                "incidents_by_status": {
                    "resolved": 100,
                    "in_progress": 30,
                    "reported": 20
                },
                "incidents_by_zone": {
                    "Times Square": 30,
                    "Central Park": 25
                },
                "average_response_time_minutes": 12.5,
                "resolution_rate_percent": 66.7,
                "peak_incident_hours": [14, 18, 22]
            }
        }


class IncidentTrendResponse(BaseModel):
    """Incident trend response"""
    period: str
    data_points: List[Dict[str, Any]]
    total_change_percent: Optional[float]
    trend_direction: str  # up, down, stable
    
    class Config:
        schema_extra = {
            "example": {
                "period": "daily",
                "data_points": [
                    {"date": "2026-08-01", "incidents": 5},
                    {"date": "2026-08-02", "incidents": 8}
                ],
                "total_change_percent": 15.0,
                "trend_direction": "up"
            }
        }


# ==================== USER ANALYTICS ====================

class UserAnalytics(BaseModel):
    """User analytics"""
    total_users: int
    active_users: int
    new_users: int
    users_by_role: Dict[str, int]
    users_by_country: Dict[str, int]
    daily_active_users: int
    monthly_active_users: int
    user_retention_rate: Optional[float]
    churned_users: int
    
    class Config:
        schema_extra = {
            "example": {
                "total_users": 5000,
                "active_users": 3500,
                "new_users": 250,
                "users_by_role": {
                    "tourist": 4000,
                    "hotel": 600,
                    "police": 200,
                    "hospital": 100
                },
                "users_by_country": {
                    "USA": 2000,
                    "UK": 1000,
                    "Canada": 500
                },
                "daily_active_users": 1200,
                "monthly_active_users": 2800,
                "user_retention_rate": 75.5,
                "churned_users": 120
            }
        }


# ==================== LOCATION ANALYTICS ====================

class LocationAnalytics(BaseModel):
    """Location analytics"""
    total_location_updates: int
    active_tracking_users: int
    geofences_created: int
    geofence_violations: int
    safe_zones_visited: int
    average_update_frequency: float
    most_visited_zones: List[Dict[str, Any]]
    high_risk_areas: List[Dict[str, Any]]
    
    class Config:
        schema_extra = {
            "example": {
                "total_location_updates": 50000,
                "active_tracking_users": 800,
                "geofences_created": 50,
                "geofence_violations": 12,
                "safe_zones_visited": 2500,
                "average_update_frequency": 30.5,
                "most_visited_zones": [
                    {"zone": "Times Square", "visits": 500}
                ],
                "high_risk_areas": [
                    {"zone": "Downtown", "incidents": 20}
                ]
            }
        }


# ==================== SOS ANALYTICS ====================

class SOSAnalytics(BaseModel):
    """SOS analytics"""
    total_sos_triggered: int
    active_sos: int
    sos_by_priority: Dict[str, int]
    sos_by_service: Dict[str, int]
    average_response_time_minutes: Optional[float]
    assisted_count: int
    assistance_success_rate: Optional[float]
    peak_sos_hours: Optional[List[int]]
    average_user_satisfaction: Optional[float]
    
    class Config:
        schema_extra = {
            "example": {
                "total_sos_triggered": 100,
                "active_sos": 5,
                "sos_by_priority": {
                    "critical": 20,
                    "high": 50,
                    "medium": 20,
                    "low": 10
                },
                "sos_by_service": {
                    "police": 40,
                    "ambulance": 35,
                    "fire": 15
                },
                "average_response_time_minutes": 8.5,
                "assisted_count": 85,
                "assistance_success_rate": 85.0,
                "peak_sos_hours": [15, 18, 22],
                "average_user_satisfaction": 4.2
            }
        }


# ==================== NOTIFICATION ANALYTICS ====================

class NotificationAnalytics(BaseModel):
    """Notification analytics"""
    total_sent: int
    total_delivered: int
    total_read: int
    total_failed: int
    delivery_rate_percent: float
    read_rate_percent: float
    notifications_by_type: Dict[str, int]
    notifications_by_channel: Dict[str, int]
    notifications_by_priority: Dict[str, int]
    average_delivery_time_seconds: Optional[float]
    
    class Config:
        schema_extra = {
            "example": {
                "total_sent": 5000,
                "total_delivered": 4750,
                "total_read": 3800,
                "total_failed": 250,
                "delivery_rate_percent": 95.0,
                "read_rate_percent": 80.0,
                "notifications_by_type": {
                    "emergency_alert": 500,
                    "incident_update": 2000
                },
                "notifications_by_channel": {
                    "push": 3000,
                    "sms": 1500,
                    "email": 500
                },
                "average_delivery_time_seconds": 2.3
            }
        }


# ==================== SAFETY SCORE ====================

class SafetyScore(BaseModel):
    """Safety score metrics"""
    overall_score: float = Field(..., ge=0, le=100)
    score_by_category: Dict[str, float]
    score_by_zone: Dict[str, float]
    score_trend: Optional[str]  # improving, stable, declining
    last_updated: datetime
    factors_contributing_positively: List[str]
    factors_contributing_negatively: List[str]
    recommendations: List[str]
    
    class Config:
        schema_extra = {
            "example": {
                "overall_score": 72.5,
                "score_by_category": {
                    "theft": 65.0,
                    "assault": 75.0,
                    "medical_emergency": 80.0
                },
                "score_by_zone": {
                    "Times Square": 70.0,
                    "Central Park": 75.0
                },
                "score_trend": "improving",
                "factors_contributing_positively": [
                    "Increased police presence",
                    "Community awareness programs"
                ],
                "factors_contributing_negatively": [
                    "Rising tourist numbers",
                    "Limited lighting in some areas"
                ],
                "recommendations": [
                    "Increase patrols in high-risk areas",
                    "Improve street lighting"
                ]
            }
        }


# ==================== DASHBOARD WIDGETS ====================

class DashboardWidget(BaseModel):
    """Dashboard widget"""
    widget_id: str
    widget_type: str
    title: str
    chart_type: Optional[str] = None
    data: Dict[str, Any]
    refresh_interval_seconds: int = 300
    is_favorite: bool = False


class DashboardConfiguration(BaseModel):
    """Dashboard configuration"""
    dashboard_id: str
    user_id: int
    name: str
    widgets: List[DashboardWidget]
    layout: Optional[str] = None  # grid, list, etc.
    is_public: bool = False
    created_at: datetime
    updated_at: datetime


class DashboardWidgetResponse(BaseModel):
    """Dashboard widget response"""
    widget_id: str
    widget_type: str
    title: str
    chart_type: Optional[str]
    data: Dict[str, Any]
    generated_at: datetime
    
    class Config:
        from_attributes = True


# ==================== REPORT GENERATION ====================

class ReportTypeEnum(str):
    """Report types"""
    INCIDENT_SUMMARY = "incident_summary"
    SAFETY_ANALYSIS = "safety_analysis"
    USER_ACTIVITY = "user_activity"
    OPERATIONAL = "operational"
    STATISTICAL = "statistical"
    CUSTOM = "custom"


class ReportFormatEnum(str):
    """Report formats"""
    PDF = "pdf"
    EXCEL = "excel"
    JSON = "json"
    CSV = "csv"
    HTML = "html"


class ReportGenerationRequest(BaseModel):
    """Request to generate report"""
    report_type: str
    format: str = "pdf"
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    include_charts: bool = True
    include_summary: bool = True
    include_recommendations: bool = True
    filters: Optional[Dict[str, Any]] = None
    email_recipient: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "report_type": "incident_summary",
                "format": "pdf",
                "start_date": "2026-08-01T00:00:00",
                "end_date": "2026-08-31T23:59:59",
                "include_charts": True,
                "include_summary": True,
                "email_recipient": "admin@example.com"
            }
        }


class ReportResponse(BaseModel):
    """Report response"""
    report_id: str
    report_type: str
    format: str
    file_url: str
    file_size_mb: float
    generated_at: datetime
    generated_by_id: int
    expires_at: datetime
    is_ready: bool
    status: str  # generating, ready, failed
    
    class Config:
        from_attributes = True


class ScheduledReportCreate(BaseModel):
    """Create scheduled report"""
    name: str
    report_type: str
    format: str = "pdf"
    frequency: str  # daily, weekly, monthly
    day_of_week: Optional[str] = None
    day_of_month: Optional[int] = None
    send_time: str = "08:00"  # HH:MM format
    email_recipients: List[str]
    include_charts: bool = True
    filters: Optional[Dict[str, Any]] = None
    is_active: bool = True


class ScheduledReportResponse(BaseModel):
    """Scheduled report response"""
    id: int
    name: str
    report_type: str
    format: str
    frequency: str
    next_generation: datetime
    last_generated: Optional[datetime]
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ==================== EXPORT ====================

class ExportRequest(BaseModel):
    """Export data request"""
    data_type: str
    format: str = Field(..., pattern="^(csv|json|excel|pdf)$")
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    filters: Optional[Dict[str, Any]] = None
    include_media: bool = False
    
    class Config:
        schema_extra = {
            "example": {
                "data_type": "incidents",
                "format": "csv",
                "start_date": "2026-08-01T00:00:00",
                "end_date": "2026-08-31T23:59:59"
            }
        }


class ExportResponse(BaseModel):
    """Export response"""
    export_id: str
    file_url: str
    file_size_mb: float
    total_records: int
    created_at: datetime
    expires_at: datetime
    
    class Config:
        schema_extra = {
            "example": {
                "export_id": "export_123",
                "file_url": "https://example.com/exports/export_123.csv",
                "file_size_mb": 5.2,
                "total_records": 500,
                "created_at": "2026-08-26T10:30:00",
                "expires_at": "2026-09-26T10:30:00"
            }
        }


# ==================== COMPARISON ====================

class ComparisonRequest(BaseModel):
    """Compare metrics between periods"""
    metric: str
    period_1_start: datetime
    period_1_end: datetime
    period_2_start: datetime
    period_2_end: datetime
    group_by: Optional[str] = None


class ComparisonResponse(BaseModel):
    """Comparison response"""
    metric: str
    period_1: Dict[str, Any]
    period_2: Dict[str, Any]
    change_percent: float
    change_direction: str  # up, down, stable
    
    class Config:
        schema_extra = {
            "example": {
                "metric": "total_incidents",
                "period_1": {"value": 100, "date_range": "Aug 1-15"},
                "period_2": {"value": 120, "date_range": "Aug 16-31"},
                "change_percent": 20.0,
                "change_direction": "up"
            }
        }


# ==================== HEALTH CHECK ANALYTICS ====================

class SystemHealthAnalytics(BaseModel):
    """System health analytics"""
    api_uptime_percent: float
    average_response_time_ms: float
    error_rate_percent: float
    total_requests: int
    failed_requests: int
    database_connection_status: str
    cache_hit_rate: Optional[float]
    last_check: datetime
    
    class Config:
        schema_extra = {
            "example": {
                "api_uptime_percent": 99.9,
                "average_response_time_ms": 125.5,
                "error_rate_percent": 0.1,
                "total_requests": 50000,
                "failed_requests": 50,
                "database_connection_status": "healthy",
                "cache_hit_rate": 85.5,
                "last_check": "2026-08-26T10:30:00"
            }
        }
