"""
Attendance CRUD Handler
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from crud.base import CRUDBase
from models.attendance import AttendanceRecord


class AttendanceCrudHandler(CRUDBase[AttendanceRecord, None, None]):
    """CRUD operations for Attendance Records"""

    def create_attendance_record(
        self, db: Session, obj_in: Dict[str, Any]
    ) -> AttendanceRecord:
        """Create a new attendance record (clock in)"""
        return super().create(db, obj_in)

    def get_active_attendance_by_employee(
        self, db: Session, employee_id: str
    ) -> Optional[AttendanceRecord]:
        """Get active attendance record (clocked in but not clocked out) for an employee"""
        return (
            db.query(self.model)
            .filter(
                and_(
                    AttendanceRecord.employee_id == employee_id,
                    AttendanceRecord.clock_out.is_(None)
                )
            )
            .order_by(desc(AttendanceRecord.clock_in))
            .first()
        )


attendance_crud_handler = AttendanceCrudHandler(AttendanceRecord)

