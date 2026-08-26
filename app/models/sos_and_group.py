"""
Database models for SOS/Emergency and Tourist Group Coordination.
Handles emergency assistance triggers and group-based safety coordination.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Enum, ForeignKey, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()


class SOSStatus(str, enum.Enum):
    """Status of SOS requests"""
    TRIGGERED = "triggered"
    ACKNOWLEDGED = "acknowledged"
    DISPATCHED = "dispatched"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CANCELLED = "cancelled"


class SOSPriority(str, enum.Enum):
    """Priority levels for SOS"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class EmergencyServiceType(str, enum.Enum):
    """Types of emergency services"""
    POLICE = "police"
    AMBULANCE = "ambulance"
    FIRE = "fire"
    HOSPITAL = "hospital"
    EMBASSY = "embassy"
    HELPLINE = "helpline"
    ALL = "all"


class SOSRecord(Base):
    """
    SOS (Save Our Souls) emergency assistance records.
    Triggered when tourists are in immediate danger.
    """
    __tablename__ = "sos_records"
    
    id = Column(Integer, primary_key=True, index=True)
    sos_id = Column(String(50), unique=True, index=True, nullable=False)
    
    # User Information
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    user_name = Column(String(100), nullable=False)
    user_phone = Column(String(20), nullable=False)
    
    # SOS Details
    reason = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    priority = Column(Enum(SOSPriority), default=SOSPriority.CRITICAL, index=True)
    status = Column(Enum(SOSStatus), default=SOSStatus.TRIGGERED, index=True)
    
    # Location Information
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    altitude = Column(Float, nullable=True)
    accuracy_meters = Column(Float, nullable=True)
    address = Column(String(500), nullable=True)
    
    # Emergency Services Response
    services_requested = Column(String(100), nullable=True)  # Comma-separated
    services_notified = Column(Boolean, default=False)
    services_dispatched = Column(Boolean, default=False)
    dispatch_time = Column(DateTime, nullable=True)
    
    # Emergency Contacts Notification
    emergency_contacts_notified = Column(Boolean, default=False)
    emergency_contacts_notified_at = Column(DateTime, nullable=True)
    
    # Response Information
    responded_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    responded_at = Column(DateTime, nullable=True)
    response_notes = Column(Text, nullable=True)
    estimated_arrival_minutes = Column(Integer, nullable=True)
    
    # Resolution
    resolved_at = Column(DateTime, nullable=True)
    resolution_notes = Column(Text, nullable=True)
    assistance_provided = Column(Boolean, default=False)
    
    # Feedback
    user_satisfaction = Column(Integer, nullable=True)  # 1-5 scale
    feedback = Column(Text, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    triggered_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="sos_records")
    updates = relationship("SOSUpdate", back_populates="sos_record", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<SOSRecord(id={self.sos_id}, user_id={self.user_id}, status={self.status})>"


class SOSUpdate(Base):
    """
    Real-time updates for SOS records.
    Tracks status changes and communications during emergency.
    """
    __tablename__ = "sos_updates"
    
    id = Column(Integer, primary_key=True, index=True)
    sos_id = Column(Integer, ForeignKey("sos_records.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Update Information
    update_type = Column(String(100), nullable=False)  # status_change, dispatch, arrival, etc.
    update_message = Column(Text, nullable=False)
    old_status = Column(Enum(SOSStatus), nullable=True)
    new_status = Column(Enum(SOSStatus), nullable=True)
    
    # Location Update
    updated_latitude = Column(Float, nullable=True)
    updated_longitude = Column(Float, nullable=True)
    
    # Source of Update
    updated_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    update_source = Column(String(50), nullable=True)  # mobile_app, web, emergency_service, etc.
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    sos_record = relationship("SOSRecord", back_populates="updates")
    
    def __repr__(self):
        return f"<SOSUpdate(id={self.id}, sos_id={self.sos_id}, type={self.update_type})>"


class TouristGroup(Base):
    """
    Groups of tourists traveling together.
    Enables shared safety features and group coordination.
    """
    __tablename__ = "tourist_groups"
    
    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(String(50), unique=True, index=True, nullable=False)
    
    # Group Information
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    join_code = Column(String(20), unique=True, index=True, nullable=False)
    
    # Group Leader/Admin
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Group Details
    total_members = Column(Integer, default=1)
    max_members = Column(Integer, nullable=True)
    
    # Travel Information
    destination = Column(String(255), nullable=True)
    travel_start_date = Column(DateTime, nullable=True)
    travel_end_date = Column(DateTime, nullable=True)
    
    # Shared Safety Features
    share_location = Column(Boolean, default=True)
    share_check_in = Column(Boolean, default=True)
    enable_group_sos = Column(Boolean, default=True)
    enable_panic_alert = Column(Boolean, default=True)
    
    # Location Sharing
    location_update_interval_seconds = Column(Integer, default=60)
    last_location_update = Column(DateTime, nullable=True)
    
    # Group Status
    is_active = Column(Boolean, default=True, index=True)
    status = Column(String(50), default="active")  # active, inactive, completed
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    members = relationship("GroupMember", back_populates="group", cascade="all, delete-orphan")
    locations = relationship("GroupLocation", back_populates="group", cascade="all, delete-orphan")
    panic_alerts = relationship("GroupPanicAlert", back_populates="group", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<TouristGroup(id={self.group_id}, name={self.name}, members={self.total_members})>"


class GroupMember(Base):
    """
    Members of a tourist group.
    """
    __tablename__ = "group_members"
    
    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("tourist_groups.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Member Role
    is_admin = Column(Boolean, default=False)
    is_leader = Column(Boolean, default=False)
    
    # Member Status
    join_status = Column(String(50), default="active")  # active, left, removed
    joined_at = Column(DateTime, default=datetime.utcnow)
    left_at = Column(DateTime, nullable=True)
    
    # Permissions
    can_share_location = Column(Boolean, default=True)
    can_send_alerts = Column(Boolean, default=True)
    can_manage_members = Column(Boolean, default=False)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    group = relationship("TouristGroup", back_populates="members")
    user = relationship("User", back_populates="group_memberships")
    
    def __repr__(self):
        return f"<GroupMember(group_id={self.group_id}, user_id={self.user_id})>"


class GroupLocation(Base):
    """
    Shared location tracking for group members.
    """
    __tablename__ = "group_locations"
    
    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("tourist_groups.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Location Data
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    accuracy_meters = Column(Float, nullable=True)
    address = Column(String(500), nullable=True)
    
    # Status
    is_latest = Column(Boolean, default=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    group = relationship("TouristGroup", back_populates="locations")
    
    def __repr__(self):
        return f"<GroupLocation(group_id={self.group_id}, user_id={self.user_id})>"


class GroupPanicAlert(Base):
    """
    Panic alerts triggered by group members.
    Notifies entire group of emergency situation.
    """
    __tablename__ = "group_panic_alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(String(50), unique=True, index=True, nullable=False)
    
    # Alert Information
    group_id = Column(Integer, ForeignKey("tourist_groups.id", ondelete="CASCADE"), nullable=False, index=True)
    triggered_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Alert Details
    reason = Column(Text, nullable=True)
    severity = Column(String(50), default="high")
    
    # Location at Alert Time
    alert_latitude = Column(Float, nullable=False)
    alert_longitude = Column(Float, nullable=False)
    alert_address = Column(String(500), nullable=True)
    
    # Response
    members_notified_count = Column(Integer, default=0)
    members_acknowledged_count = Column(Integer, default=0)
    emergency_services_called = Column(Boolean, default=False)
    
    # Resolution
    resolved = Column(Boolean, default=False)
    resolved_at = Column(DateTime, nullable=True)
    resolution_notes = Column(Text, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    group = relationship("TouristGroup", back_populates="panic_alerts")
    
    def __repr__(self):
        return f"<GroupPanicAlert(id={self.alert_id}, group_id={self.group_id})>"


class GroupCheckIn(Base):
    """
    Check-in records for group members.
    Confirms member safety at regular intervals.
    """
    __tablename__ = "group_check_ins"
    
    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("tourist_groups.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Check-in Status
    status = Column(String(50), nullable=False)  # safe, need_help, emergency
    message = Column(Text, nullable=True)
    
    # Location at Check-in
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    address = Column(String(500), nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f"<GroupCheckIn(group_id={self.group_id}, user_id={self.user_id}, status={self.status})>"
