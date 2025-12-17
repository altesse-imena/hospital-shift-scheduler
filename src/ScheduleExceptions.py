from datetime import datetime

class SchedulingException(Exception):
    """Base exception for scheduling errors with logging and context."""
    def __init__(self, message, error_code=None, context=None):
        self.message = message
        self.error_code = error_code or "E000: Assignment Time Error"
        self.context = context or {}
        self.timestamp = datetime.now()
        super().__init__(f"[{self.error_code}] {message}")

class InvalidScheduleException(SchedulingException):
    """Raised when schedules clash."""
    def __init__(self, message, staff=None, shift=None):
        context = {
            'staff_name': staff.get_name() if staff else None,
            'shift_name': shift.get_name() if shift else None
        }
        super().__init__(message, "E001: Schedule Violation", context)

class MissingStaffException(SchedulingException):
    """Raised when staff aren't around."""
    def __init__(self, message, shift=None, required_role=None):
        context = {
            'shift_name': shift.get_name() if shift else None,
            'required_role': required_role
        }
        super().__init__(message, "E003: STaff Unavailable", context)

class AvailabilityConflictException(SchedulingException):
    """Raised when staff availability clash with assignment."""
    def __init__(self, message, staff=None, shift=None):
        context = {
            'staff_name': staff.get_name() if staff else None,
            'shift_name': shift.get_name() if shift else None
        }
        super().__init__(message, "E005: Staff Assignment Error", context)