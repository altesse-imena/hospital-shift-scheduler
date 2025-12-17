from staff import Staff
from shift import Shift
from ScheduleExceptions import InvalidScheduleException, MissingStaffException, AvailabilityConflictException
from concurrent.futures import ThreadPoolExecutor, as_completed

class ParallelValidator:
    
    def __init__(self, max_workers=None):
        self.max_workers = max_workers
        self.stats = {'total': 0, 'parallel': 0}
    
    def validate_staff(self, staff_list, shift):
        self.stats['total'] += 1
        
        if len(staff_list) > 5:
            self.stats['parallel'] += 1
            return self._parallel_validation(staff_list, shift)
        return self._sequential_validation(staff_list, shift)
    
    def _parallel_validation(self, staff_list, shift):
        eligible, conflicts = [], []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_staff = {
                executor.submit(self._validate_single, staff, shift): staff
                for staff in staff_list
            }
            
            for future in as_completed(future_to_staff):
                staff = future_to_staff[future]
                try:
                    result = future.result()
                    if result['is_eligible']:
                        eligible.append(staff)
                    if result['conflict']:
                        conflicts.append(result['conflict'])
                except Exception as exc:
                    conflicts.append({'type': 'error', 'message': str(exc)})
        
        return {'eligible': eligible, 'conflicts': conflicts}
    
    def _sequential_validation(self, staff_list, shift):
        """Perform sequential validation (fallback for small lists)."""
        eligible, conflicts = [], []
        
        for staff in staff_list:
            result = self._validate_single(staff, shift)
            if result['is_eligible']:
                eligible.append(staff)
            if result['conflict']:
                conflicts.append(result['conflict'])
        
        return {'eligible': eligible, 'conflicts': conflicts}
    
    def _validate_single(self, staff, shift):
        """Validate a single staff member for a shift."""
        if staff.get_role() != shift.get_required_role():
            return {'is_eligible': False, 'conflict': {'type': 'role_mismatch'}}
        
        if not staff.is_available_for_shift(shift.get_name()):
            return {'is_eligible': False, 'conflict': {'type': 'availability'}}
        
        if staff.is_already_assigned_to_shift(shift.get_name()):
            return {'is_eligible': False, 'conflict': {'type': 'double_booking'}}
        
        return {'is_eligible': True, 'conflict': None}
    
    def get_statistics(self):
        """Get validation performance statistics."""
        return {
            'total': self.stats['total'],
            'parallel': self.stats['parallel'],
            'sequential': self.stats['total'] - self.stats['parallel']
        }


class ScheduleManager:
    def __init__(self, staff_list, shift_list):
        self.staff_list = staff_list
        self.shift_list = shift_list
        self.errors = []
        self.validator = ParallelValidator()
    
    def assign_shifts(self):
        """Assign shifts to staff with parallel validation and exception handling."""
        try:
            for shift in self.shift_list:
                self._process_shift(shift)
            return len(self.errors) == 0
        except Exception as e:
            self.errors.append(f"Unexpected error: {str(e)}")
            return False
    
    def _process_shift(self, shift):
        """Process a single shift assignment."""
        results = self.validator.validate_staff(self.staff_list, shift)
        eligible = results['eligible']
        
        if not eligible:
            raise MissingStaffException(
                f"No eligible staff for {shift.get_name()}",
                shift, shift.get_required_role()
            )
        
        eligible.sort(key=lambda s: s.get_assignment_count())
        assigned = 0
        
        for staff in eligible:
            if assigned >= shift.get_required_count():
                break
            
            try:
                self._assign_staff(staff, shift)
                assigned += 1
            except AvailabilityConflictException as e:
                self.errors.append(e)
        
        if shift.get_shortage() > 0:
            raise MissingStaffException(
                f"Shortage for {shift.get_name()}",
                shift, shift.get_required_role()
            )
    
    def _assign_staff(self, staff, shift):
        """Assign staff to shift with validation."""
        if not staff.is_available_for_shift(shift.get_name()):
            raise AvailabilityConflictException(
                f"{staff.get_name()} not available",
                staff, shift
            )
        
        staff.add_assigned_shift(shift.get_name())
        shift.add_staff(staff)
    
    def get_errors(self):
        return self.errors
    
    def print_schedule(self):
        print("\n=== SHIFT SCHEDULE ===\n")
        for shift in self.shift_list:
            print(f"Shift: {shift.get_name()} (Role: {shift.get_required_role()})")
            print(f"  Required: {shift.get_required_count()}")
            assigned = shift.get_assigned_staff()
            if assigned:
                print(f"  Assigned Staff:")
                for staff in assigned:
                    print(f"    - {staff.get_name()} (ID: {staff.get_id()})")
            else:
                print(f"  Assigned Staff: None")
            
            if shift.get_shortage() > 0:
                print(f"  ✗  SHORTAGE: {shift.get_shortage()} staff needed")
            print()
    
    def print_staff_assignments(self):
        print("\n=== STAFF ASSIGNMENTS ===\n")
        for staff in self.staff_list:
            print(f"{staff.get_name()} (ID: {staff.get_id()}, Role: {staff.get_role()})")
            assignments = staff.get_assigned_shifts()
            if assignments:
                print(f"  Assigned to: {', '.join(assignments)}")
            else:
                print(f"  Assigned to: None")
            print()