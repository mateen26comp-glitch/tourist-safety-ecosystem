"""
Database models for Location, Geofencing, and Safety Zones.
Handles user locations, geofence alerts, and safety zone management.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Enum, ForeignKey, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()


class GeofenceAlertType(str, enum.Enum):
    """Types of geofence alerts"""
    ENTERING = "entering"
    EXITING = "exiting"
    INSIDE = "inside"
    OUTSIDE = "outside"


class SafeZoneType(str, enum.Enum):
    """Types of safe zones"""
    POLICE_STATION = "police_station"
    HOSPITAL = "hospital"
    EMBASSY = "embassy"
    HELPDESK = "helpdesk"
    HOTEL = "hotel"
    TOURIST_CENTER = "tourist_center"
    GOVERNMENT_OFFICE = "government_office"
    FIRE_STATION = "fire_station"
    ATM = "atm"
    PHARMACY = "pharmacy"


class RiskLevel(str, enum.Enum):
    """Risk levels for zones"""
    SAFE = "safe"
    LOW_RISK = "low_risk"
    MEDIUM_RISK = "medium_risk"
    HIGH_RISK = "high_risk"
    RESTRICTED = "restricted"


class UserLocation(Base):
    """
    Tracks real-time location updates from users.
    Stores GPS coordinates for live tracking and geofencing.
    """
    __tablename__ = "user_locations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Location Coordinates
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    accuracy_meters = Column(Float, nullable=True)
    altitude_meters = Column(Float, nullable=True)
    
    # Location Information
    address = Column(String(500), nullable=True)
    zone_name = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    
    # Tracking Information
    is_active = Column(Boolean, default=True)
    is_real_time = Column(Boolean, default=False)  # Active real-time tracking
    
    # Device Information
    device_id = Column(String(100), nullable=True)
    device_type = Column(String(50), nullable=True)  # mobile, web, etc.
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)
    
    # Relationships
    user = relationship("User", back_populates="locations")
    
    def __repr__(self):
        return f"<UserLocation(id={self.id}, user_id={self.user_id}, lat={self.latitude}, lon={self.longitude})>"


class Geofence(Base):
    """
    Defines geofenced zones for alerts.
    Each geofence triggers alerts when users enter/exit.
    """
    __tablename__ = "geofences"
    
    id = Column(Integer, primary_key=True, index=True)
    geofence_id = Column(String(50), unique=True, index=True, nullable=False)
    
    # Geofence Details
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    zone_type = Column(String(100), nullable=True)  # High-risk zone, Safe zone, etc.
    
    # Location & Boundaries
    center_latitude = Column(Float, nullable=False)
    center_longitude = Column(Float, nullable=False)
    radius_kilometers = Column(Float, nullable=False)
    
    # Risk Assessment
    risk_level = Column(Enum(RiskLevel), default=RiskLevel.SAFE, index=True)
    risk_score = Column(Float, nullable=True)  # 0-100 scale
    risk_description = Column(Text, nullable=True)
    
    # Alert Configuration
    alert_enabled = Column(Boolean, default=True)
    send_entry_alert = Column(Boolean, default=True)
    send_exit_alert = Column(Boolean, default=False)
    alert_message = Column(Text, nullable=True)
    
    # Notification Settings
    notification_channels = Column(String(100), default="push,email")  # push, sms, email
    
    # Admin Information
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    managed_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True, index=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Geofence(id={self.geofence_id}, name={self.name}, risk={self.risk_level})>"


class GeofenceAlert(Base):
    """
    Records geofence alerts when users trigger boundary crossings.
    """
    __tablename__ = "geofence_alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(String(50), unique=True, index=True, nullable=False)
    
    # Alert Information
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    geofence_id = Column(Integer, ForeignKey("geofences.id"), nullable=False, index=True)
    
    # Alert Type & Status
    alert_type = Column(Enum(GeofenceAlertType), nullable=False)
    is_acknowledged = Column(Boolean, default=False)
    acknowledged_at = Column(DateTime, nullable=True)
    acknowledged_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Location at Alert Time
    alert_latitude = Column(Float, nullable=False)
    alert_longitude = Column(Float, nullable=False)
    
    # Alert Response
    user_response = Column(String(255), nullable=True)  # e.g., "Safe", "Need Help"
    response_received_at = Column(DateTime, nullable=True)
    
    # Notification Status
    notification_sent = Column(Boolean, default=False)
    notification_channels_used = Column(String(100), nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f"<GeofenceAlert(id={self.alert_id}, user_id={self.user_id}, type={self.alert_type})>"


class SafeZone(Base):
    """
    Predefined safe zones (hospitals, police stations, embassies, etc.)
    that tourists can use for assistance.
    """
    __tablename__ = "safe_zones"
    
    id = Column(Integer, primary_key=True, index=True)
    zone_id = Column(String(50), unique=True, index=True, nullable=False)
    
    # Zone Information
    name = Column(String(255), nullable=False)
    zone_type = Column(Enum(SafeZoneType), nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Location
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    address = Column(String(500), nullable=True)
    city = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    
    # Contact Information
    primary_phone = Column(String(20), nullable=True)
    emergency_phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    website = Column(String(255), nullable=True)
    
    # Operational Details
    operating_hours = Column(JSON, default={})  # {day: {open: time, close: time}}
    languages_spoken = Column(String(255), nullable=True)
    services_available = Column(JSON, default={})
    
    # Classification
    is_24_7 = Column(Boolean, default=False)
    verification_status = Column(String(50), default="verified")
    rating = Column(Float, nullable=True)  # 0-5 stars
    reviews_count = Column(Integer, default=0)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_verified_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<SafeZone(id={self.zone_id}, name={self.name}, type={self.zone_type})>"


class NearbyAssistanceLog(Base):
    """
    Logs when tourists search for nearby assistance.
    Used for analytics and to understand assistance-seeking patterns.
    """
    __tablename__ = "nearby_assistance_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Search Information
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    search_latitude = Column(Float, nullable=False)
    search_longitude = Column(Float, nullable=False)
    search_radius_km = Column(Float, nullable=True)
    
    # Results
    assistance_type = Column(String(100), nullable=True)  # hospital, police, embassy, etc.
    results_found_count = Column(Integer, default=0)
    
    # Selected Zone
    selected_zone_id = Column(Integer, ForeignKey("safe_zones.id"), nullable=True)
    selected_at = Column(DateTime, nullable=True)
    
    # User Status
    user_safe = Column(Boolean, nullable=True)
    assistance_obtained = Column(Boolean, default=False)
    assistance_obtained_at = Column(DateTime, nullable=True)
    
    # Feedback
    feedback = Column(Text, nullable=True)
    rating = Column(Integer, nullable=True)  # 1-5
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f"<NearbyAssistanceLog(id={self.id}, user_id={self.user_id}, type={self.assistance_type})>"


class LocationAnalytics(Base):
    """
    Aggregated location-based analytics.
    Used for heatmaps and geographic analysis.
    """
    __tablename__ = "location_analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Time Period
    date = Column(DateTime, default=datetime.utcnow, unique=True, index=True)
    
    # Tracking Data
    active_users_count = Column(Integer, default=0)
    locations_tracked = Column(Integer, default=0)
    average_location_accuracy = Column(Float, nullable=True)
    
    # Geofence Data
    geofence_alerts_count = Column(Integer, default=0)
    alerts_by_type = Column(JSON, default={})  # {alert_type: count}
    
    # Risk Zone Data
    high_risk_zone_visits = Column(Integer, default=0)
    restricted_zone_incidents = Column(Integer, default=0)
    
    # Assistance Data
    assistance_searches = Column(Integer, default=0)
    assistance_obtained = Column(Integer, default=0)
    
    # Heatmap Data
    zone_visit_counts = Column(JSON, default={})  # {zone: visit_count}
    incident_density_map = Column(JSON, default={})  # Geospatial incident density
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<LocationAnalytics(date={self.date}, active_users={self.active_users_count})>"
