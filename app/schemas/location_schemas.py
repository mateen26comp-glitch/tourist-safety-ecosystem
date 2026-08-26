"""
Pydantic schemas for Location tracking and Geofencing endpoints.
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, validator
from app.schemas.common_schemas import TimestampMixin, LocationBase


# ==================== LOCATION TRACKING ====================

class LocationUpdateRequest(BaseModel):
    """Real-time location update"""
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    accuracy_meters: Optional[float] = None
    altitude_meters: Optional[float] = None
    speed_kmh: Optional[float] = None
    heading_degrees: Optional[float] = None
    device_id: Optional[str] = None
    device_type: Optional[str] = None  # mobile, web, wearable, etc.
    timestamp: Optional[datetime] = None
    
    class Config:
        schema_extra = {
            "example": {
                "latitude": 40.7128,
                "longitude": -74.0060,
                "accuracy_meters": 10.5,
                "altitude_meters": 50.0,
                "speed_kmh": 5.2,
                "heading_degrees": 180.0,
                "device_id": "device_123",
                "device_type": "mobile"
            }
        }


class LocationResponse(LocationBase, TimestampMixin):
    """Location response"""
    id: int
    user_id: int
    device_id: Optional[str]
    device_type: Optional[str]
    speed_kmh: Optional[float]
    heading_degrees: Optional[float]
    is_real_time: bool
    accuracy_meters: Optional[float]
    
    class Config:
        from_attributes = True


class LocationHistoryRequest(BaseModel):
    """Location history request"""
    user_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    skip: int = 0
    limit: int = 100
    
    class Config:
        schema_extra = {
            "example": {
                "start_date": "2026-08-01T00:00:00",
                "end_date": "2026-08-31T23:59:59",
                "skip": 0,
                "limit": 50
            }
        }


class LocationHistoryResponse(BaseModel):
    """Location history response"""
    total: int
    locations: List[LocationResponse]
    start_date: datetime
    end_date: datetime
    
    class Config:
        schema_extra = {
            "example": {
                "total": 150,
                "locations": [],
                "start_date": "2026-08-01T00:00:00",
                "end_date": "2026-08-31T23:59:59"
            }
        }


class LocationTrail(BaseModel):
    """User location trail/route"""
    user_id: int
    start_time: datetime
    end_time: datetime
    total_distance_km: float
    average_speed_kmh: float
    waypoints: List[LocationBase]
    
    class Config:
        from_attributes = True


# ==================== GEOFENCE TYPES ====================

class GeofenceShapeEnum(str):
    """Geofence shape types"""
    CIRCLE = "circle"
    POLYGON = "polygon"
    RECTANGLE = "rectangle"


class GeofenceAlertTypeEnum(str):
    """Geofence alert types"""
    ENTRY = "entry"
    EXIT = "exit"
    BOTH = "both"
    DWELL = "dwell"


# ==================== GEOFENCE ====================

class GeofenceBase(BaseModel):
    """Base geofence"""
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    is_active: bool = True
    alert_type: str = "both"  # entry, exit, both, dwell
    dwell_time_seconds: Optional[int] = None
    notify_user: bool = True
    notify_emergency_contacts: bool = False
    notify_authorities: bool = False


class CircleGeofenceCreate(GeofenceBase):
    """Create circular geofence"""
    center_latitude: float = Field(..., ge=-90, le=90)
    center_longitude: float = Field(..., ge=-180, le=180)
    radius_meters: float = Field(..., gt=0, le=50000)


class PolygonGeofenceCreate(GeofenceBase):
    """Create polygon geofence"""
    vertices: List[dict] = Field(...)  # List of {latitude, longitude}
    
    @validator('vertices')
    def validate_vertices(cls, v):
        if len(v) < 3:
            raise ValueError('Polygon must have at least 3 vertices')
        for vertex in v:
            if 'latitude' not in vertex or 'longitude' not in vertex:
                raise ValueError('Each vertex must have latitude and longitude')
            if not (-90 <= vertex['latitude'] <= 90):
                raise ValueError('Invalid latitude')
            if not (-180 <= vertex['longitude'] <= 180):
                raise ValueError('Invalid longitude')
        return v


class RectangleGeofenceCreate(GeofenceBase):
    """Create rectangular geofence"""
    north_latitude: float = Field(..., ge=-90, le=90)
    south_latitude: float = Field(..., ge=-90, le=90)
    east_longitude: float = Field(..., ge=-180, le=180)
    west_longitude: float = Field(..., ge=-180, le=180)
    
    @validator('south_latitude')
    def validate_latitude(cls, v, values):
        if 'north_latitude' in values and v >= values['north_latitude']:
            raise ValueError('South latitude must be less than north latitude')
        return v
    
    @validator('west_longitude')
    def validate_longitude(cls, v, values):
        if 'east_longitude' in values and v >= values['east_longitude']:
            raise ValueError('West longitude must be less than east longitude')
        return v


class GeofenceUpdate(BaseModel):
    """Update geofence"""
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    alert_type: Optional[str] = None
    dwell_time_seconds: Optional[int] = None
    notify_user: Optional[bool] = None
    notify_emergency_contacts: Optional[bool] = None
    notify_authorities: Optional[bool] = None


class GeofenceResponse(GeofenceBase, TimestampMixin):
    """Geofence response"""
    id: int
    geofence_id: str
    user_id: int
    shape: str
    zone_name: Optional[str]
    
    class Config:
        from_attributes = True


class GeofenceDetailResponse(GeofenceResponse):
    """Detailed geofence response"""
    violations_count: int = 0
    total_alerts: int = 0
    last_alert_at: Optional[datetime] = None


# ==================== GEOFENCE EVENTS ====================

class GeofenceEventEnum(str):
    """Geofence event types"""
    ENTRY = "entry"
    EXIT = "exit"
    DWELL = "dwell"
    LOITERING = "loitering"


class GeofenceAlertCreate(BaseModel):
    """Create geofence alert"""
    geofence_id: int
    event_type: str
    latitude: float
    longitude: float
    description: Optional[str] = None


class GeofenceAlertResponse(TimestampMixin):
    """Geofence alert response"""
    id: int
    geofence_id: int
    user_id: int
    event_type: str
    latitude: float
    longitude: float
    accuracy_meters: Optional[float]
    description: Optional[str]
    alert_sent: bool
    alert_sent_at: Optional[datetime]
    acknowledged: bool
    acknowledged_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class GeofenceViolation(BaseModel):
    """Geofence violation record"""
    id: int
    geofence_id: int
    user_id: int
    violation_type: str  # unauthorized_entry, unauthorized_exit
    latitude: float
    longitude: float
    violation_time: datetime
    severity: str  # low, medium, high
    description: Optional[str]
    reported_at: datetime


# ==================== SAFE ZONES ====================

class SafeZoneBase(BaseModel):
    """Base safe zone"""
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    radius_meters: float = Field(..., gt=0, le=10000)
    zone_type: str  # police_station, hospital, embassy, shelter, etc.
    is_verified: bool = False
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    operating_hours: Optional[str] = None
    services_available: Optional[str] = None  # Comma-separated


class SafeZoneCreate(SafeZoneBase):
    """Create safe zone"""
    pass


class SafeZoneUpdate(BaseModel):
    """Update safe zone"""
    name: Optional[str] = None
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    radius_meters: Optional[float] = None
    zone_type: Optional[str] = None
    is_verified: Optional[bool] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    operating_hours: Optional[str] = None
    services_available: Optional[str] = None


class SafeZoneResponse(SafeZoneBase, TimestampMixin):
    """Safe zone response"""
    id: int
    safe_zone_id: str
    distance_km: Optional[float] = None
    
    class Config:
        from_attributes = True


class SafeZoneNearbyRequest(BaseModel):
    """Find nearby safe zones"""
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    radius_km: float = Field(default=5.0, gt=0, le=50)
    zone_type: Optional[str] = None
    limit: int = Field(default=10, ge=1, le=100)


class SafeZoneNearbyResponse(BaseModel):
    """Nearby safe zones response"""
    total_found: int
    safe_zones: List[SafeZoneResponse]
    
    class Config:
        schema_extra = {
            "example": {
                "total_found": 3,
                "safe_zones": []
            }
        }


# ==================== LOCATION SHARING ====================

class LocationSharingRequest(BaseModel):
    """Enable location sharing with someone"""
    share_with_user_id: int
    share_duration_minutes: Optional[int] = None
    share_type: str = "real_time"  # real_time, periodic, on_demand
    update_interval_seconds: Optional[int] = None


class LocationSharingResponse(BaseModel):
    """Location sharing response"""
    id: int
    shared_by_id: int
    shared_with_id: int
    share_type: str
    is_active: bool
    expires_at: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True


class LocationSharingList(BaseModel):
    """List of active location sharings"""
    total: int
    active_sharings: List[LocationSharingResponse]


# ==================== ZONE INFORMATION ====================

class ZoneInfo(BaseModel):
    """Information about a zone/area"""
    zone_name: str
    zone_type: str  # tourist, residential, commercial, industrial
    safety_rating: float = Field(..., ge=1, le=5)
    recent_incident_count: int
    police_stations_nearby: int
    hospitals_nearby: int
    description: Optional[str]
    last_update: datetime


class ZoneInfoResponse(BaseModel):
    """Zone information response"""
    zone: ZoneInfo
    incidents_last_7_days: int
    incidents_last_30_days: int
    alerts_active: int
    safe_zones_nearby: List[SafeZoneResponse]
    
    class Config:
        schema_extra = {
            "example": {
                "zone": {
                    "zone_name": "Times Square",
                    "zone_type": "tourist",
                    "safety_rating": 4.2,
                    "recent_incident_count": 5,
                    "police_stations_nearby": 3,
                    "hospitals_nearby": 2
                },
                "incidents_last_7_days": 5,
                "incidents_last_30_days": 12,
                "alerts_active": 2,
                "safe_zones_nearby": []
            }
        }
