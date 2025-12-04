"""
Employee Model - HR Employee Table
"""
import enum
from datetime import date
from sqlalchemy import Column, String, Date, DateTime, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datastore.base_class import Base


class EmployeeStatusEnum(str, enum.Enum):
    """Employee status enumeration"""
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'
    TERMINATED = 'TERMINATED'
    ON_LEAVE = 'ON_LEAVE'


class Employee(Base):
    """
    Employee Model
    Maps to hr.employee_t table
    """
    __tablename__ = 'employee_t'
    __table_args__ = (
        {'schema': 'hr'}
    )

    id = Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid()
    )
    employee_code = Column(
        "employee_code",
        String(50),
        nullable=False,
        unique=True,
        comment="Human-readable employee code"
    )
    first_name = Column(
        "first_name",
        String(100),
        nullable=False
    )
    last_name = Column(
        "last_name",
        String(100),
        nullable=False
    )
    date_of_birth = Column(
        "date_of_birth",
        Date,
        nullable=False
    )
    email = Column(
        "email",
        String(255),
        nullable=False,
        unique=True
    )
    city = Column(
        "city",
        String(100),
        nullable=True
    )
    country = Column(
        "country",
        String(100),
        nullable=True
    )
    status = Column(
        "status",
        ENUM(EmployeeStatusEnum, name='employee_status_enum', schema='hr', create_type=False),
        nullable=False,
        default=EmployeeStatusEnum.ACTIVE,
        server_default='ACTIVE'
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

    # Relationship to attendance records
    attendance_records = relationship(
        'AttendanceRecord',
        back_populates='employee',
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f"<Employee(id={self.id}, employee_code='{self.employee_code}', name='{self.first_name} {self.last_name}')>"

    def serialize(self):
        """Serialize employee to dictionary"""
        return {
            'id': str(self.id),
            'employee_code': self.employee_code,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'email': self.email,
            'city': self.city,
            'country': self.country,
            'status': self.status.value if isinstance(self.status, EmployeeStatusEnum) else self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

