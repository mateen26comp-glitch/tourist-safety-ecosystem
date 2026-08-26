"""
Database models for Incident Management System.
Handles incident reporting, tracking, media uploads, and status management.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Enum, ForeignKey, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()


class IncidentSeverity(str, enum.Enum):
    """Severity levels for incidents"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class IncidentCategory(str, enum.Enum):
    """Categories for incident classification"""
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


class IncidentStatus(str, enum.Enum):
    """Status progression for incidents"""
    REPORTED = "reported"
    ACKNOWLEDGED = "acknowledged"
    DISPATCHED = "dispatched"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"
    CANCELLED = "cancelled"


class Incident(Base):
    """
    Main incident model for reporting and tracking safety incidents.
    """
    __tablename__ = "incidents"
    
    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(String(50), unique=True, index=True, nullable=False)  # Human-readable ID
    
    # Reporter Information
    reporter_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    reporter_name = Column(String(100), nullable=False)
    reporter_contact = Column(String(20), nullable=False)
    
    # Incident Details
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(Enum(IncidentCategory), nullable=False, index=True)
    severity = Column(Enum(IncidentSeverity), default=IncidentSeverity.MEDIUM, index=True)
    
    # Location Information
    location_latitude = Column(Float, nullable=False)
    location_longitude = Column(Float, nullable=False)
    location_address = Column(String(500), nullable=True)
    location_zone = Column(String(100), nullable=True)
    
    # Status & Assignment
    status = Column(Enum(IncidentStatus), default=IncidentStatus.REPORTED, index=True)
    assigned_to_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    assigned_at = Column(DateTime, nullable=True)
    
    # Response Information
    emergency_services_notified = Column(Boolean, default=False)
    emergency_services_type = Column(String(100), nullable=True)  # Police, Hospital, etc.
    response_time_minutes = Column(Integer, nullable=True)
    
    # AI Classification
    ai_category_prediction = Column(String(100), nullable=True)
    ai_severity_score = Column(Float, nullable=True)  # 0-1 scale
    ai_confidence = Column(Float, nullable=True)  # 0-1 scale
    
    # Additional Info
    number_of_people_affected = Column(Integer, default=1)
    injuries_reported = Column(Boolean, default=False)
    property_damage_reported = Column(Boolean, default=False)
    estimated_damage_amount = Column(Float, nullable=True)
    
    # Resolution
    resolution_description = Column(Text, nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    resolution_notes = Column(Text, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    reporter = relationship("User", foreign_keys=[reporter_id], back_populates="incidents")
    assigned_to = relationship("User", foreign_keys=[assigned_to_id])
    media = relationship("IncidentMedia", back_populates="incident", cascade="all, delete-orphan")
    status_updates = relationship("IncidentStatusUpdate", back_populates="incident", cascade="all, delete-orphan")
    comments = relationship("IncidentComment", back_populates="incident", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Incident(id={self.incident_id}, category={self.category}, severity={self.severity}, status={self.status})>"


class IncidentMedia(Base):
    """
    Media files (photos, videos, audio) associated with incidents.
    """
    __tablename__ = "incident_media"
    
    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Media Information
    file_name = Column(String(255), nullable=False)
    file_url = Column(String(500), nullable=False)
    media_type = Column(String(50), nullable=False)  # image, video, audio
    file_size_mb = Column(Float, nullable=True)
    duration_seconds = Column(Integer, nullable=True)  # For video/audio
    
    # Metadata
    uploaded_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    description = Column(Text, nullable=True)
    
    # Relationships
    incident = relationship("Incident", back_populates="media")
    
    def __repr__(self):
        return f"<IncidentMedia(id={self.id}, incident_id={self.incident_id}, type={self.media_type})>"


class IncidentStatusUpdate(Base):
    """
    Tracks status changes and updates for an incident.
    Maintains audit trail of incident progression.
    """
    __tablename__ = "incident_status_updates"
    
    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Status Change
    old_status = Column(Enum(IncidentStatus), nullable=True)
    new_status = Column(Enum(IncidentStatus), nullable=False)
    
    # Update Details
    updated_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    update_reason = Column(Text, nullable=True)
    update_notes = Column(Text, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    incident = relationship("Incident", back_populates="status_updates")
    
    def __repr__(self):
        return f"<IncidentStatusUpdate(id={self.id}, incident_id={self.incident_id}, status={self.new_status})>"


class IncidentComment(Base):
    """
    Comments and notes on incidents from authorized personnel.
    """
    __tablename__ = "incident_comments"
    
    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Comment Content
    comment = Column(Text, nullable=False)
    is_internal = Column(Boolean, default=True)  # Internal note or visible to reporter
    
    # Commenter Information
    commented_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    incident = relationship("Incident", back_populates="comments")
    
    def __repr__(self):
        return f"<IncidentComment(id={self.id}, incident_id={self.incident_id})>"


class IncidentAnalytics(Base):
    """
    Aggregated analytics and insights for incidents.
    Used for dashboards and reporting.
    """
    __tablename__ = "incident_analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Time Period
    date = Column(DateTime, default=datetime.utcnow, unique=True, index=True)
    
    # Counts
    total_incidents = Column(Integer, default=0)
    incidents_by_category = Column(JSON, default={})  # {category: count}
    incidents_by_severity = Column(JSON, default={})  # {severity: count}
    incidents_by_status = Column(JSON, default={})    # {status: count}
    
    # Response Metrics
    average_response_time_minutes = Column(Float, nullable=True)
    resolved_count = Column(Integer, default=0)
    resolution_rate = Column(Float, nullable=True)  # Percentage
    
    # Geographic Data
    hotspot_locations = Column(JSON, default={})  # {zone: incident_count}
    
    # Severity Analysis
    critical_incidents = Column(Integer, default=0)
    high_incidents = Column(Integer, default=0)
    injuries_reported_count = Column(Integer, default=0)
    property_damage_count = Column(Integer, default=0)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<IncidentAnalytics(date={self.date}, total={self.total_incidents})>"
