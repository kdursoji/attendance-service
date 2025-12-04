"""
Attendance API Routes - RESTful endpoints
Following REST standards: POST /attendance/clock-in
Directly calls CRUD layer (no service layer)
"""
from datetime import datetime, timezone
from flask import Blueprint, jsonify
from datastore.deps import session_scope
from schemas.pydantic_models import (
    StandardResponse,
    AttendanceResponse,
    AttendanceData,
)
import crud
from exceptions.app_exceptions import NotFoundException, ConflictException

attendance_bp = Blueprint('attendance', __name__, url_prefix='/attendance')


@attendance_bp.route('/employees/<employee_id>/clock_in', methods=['POST'])
def clock_in(employee_id: str):
   
    with session_scope() as session:

        # need to create service layer
        # Check if employee exists
        # have to write crud layer.Just for understanding calling directly in API
        from models.employee import Employee
        employee = session.query(Employee).filter(Employee.id == employee_id).first()
        if not employee:
            raise NotFoundException(message='Employee not found.')
        
        # we should check whether this employee already has an active attendance entry
        # (clocked in without clock_out). If so, system should prevent duplicate clock-in.

        active_attendance = crud.attendance_crud_handler.get_active_attendance_by_employee(
            db=session,
            employee_id=employee_id
        )
        
        if active_attendance:
            raise ConflictException(
                message='Employee is already clocked in. Please clock out first.',
                payload={'attendance_id': str(active_attendance.id)}
            )
        
        # Create new attendance record (clock in)
        attendance_data = {
            'employee_id': employee_id,
            'clock_in': datetime.now(timezone.utc),
            'clock_out': None
        }

        ## need to create service layer
        attendance_record = crud.attendance_crud_handler.create_attendance_record(
            db=session,
            obj_in=attendance_data
        )
        
        attendance_data_response = AttendanceData(
            id=str(attendance_record.id),
            employee_id=str(attendance_record.employee_id),
            clock_in=attendance_record.clock_in,
            clock_out=attendance_record.clock_out,
            created_at=attendance_record.created_at,
            updated_at=attendance_record.updated_at
        )
        
        response = AttendanceResponse(
            status='success',
            message='Successfully clocked in.',
            data=attendance_data_response
        )
        return jsonify(response.model_dump(exclude_none=True)), 201

