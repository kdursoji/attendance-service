"""
Attendance Record Model - Attendance Record Table
"""
from sqlalchemy import Column, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datastore.base_class import Base


class AttendanceRecord(Base):
    """
    Attendance Record Model
    Maps to attendance.attendance_record_t table
    """
    __tablename__ = 'attendance_record_t'
   
    id = Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid()
    )
    employee_id = Column(
        "employee_id",
        UUID(as_uuid=True),
        ForeignKey('employee_t.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    clock_in = Column(
        "clock_in",
        DateTime(timezone=True),
        nullable=False
    )
    clock_out = Column(
        "clock_out",
        DateTime(timezone=True),
        nullable=True
    )
    created_at = Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    updated_at = Column(
        "updated_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )

    # Relationship to employee
    employee = relationship(
        'Employee',
        back_populates='attendance_records'
    )

    def __repr__(self):
        return f"<AttendanceRecord(id={self.id}, employee_id={self.employee_id}, clock_in={self.clock_in})>"

    def serialize(self):
        """Serialize attendance record to dictionary"""
        return {
            'id': str(self.id),
            'employee_id': str(self.employee_id),
            'clock_in': self.clock_in.isoformat() if self.clock_in else None,
            'clock_out': self.clock_out.isoformat() if self.clock_out else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

