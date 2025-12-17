from staff import Staff
from shift import Shift


class ScheduleManager:
    def __init__(self, staff_list, shift_list):
        self.staff_list = staff_list
        self.shift_list = shift_list
        self.conflicts = []
        self.shortages = []
    
    def assign_shifts(self):
        for shift in self.shift_list:
            eligible_staff = self._get_eligible_staff(shift)
            
            if not eligible_staff:
                self.shortages.append({
                    'shift': shift.get_name(),
                    'required_role': shift.get_required_role(),
                    'shortage': shift.get_required_count()
                })
                continue
            
            eligible_staff.sort(key=lambda s: s.get_assignment_count())
            
            assigned_count = 0
            for staff in eligible_staff:
                if assigned_count >= shift.get_required_count():
                    break
                
                conflict = self._check_conflicts(staff, shift)
                if conflict:
                    self.conflicts.append(conflict)
                    continue
                
                staff.add_assigned_shift(shift.get_name())
                shift.add_staff(staff)
                assigned_count += 1
            
            if shift.get_shortage() > 0:
                self.shortages.append({
                    'shift': shift.get_name(),
                    'required_role': shift.get_required_role(),
                    'shortage': shift.get_shortage()
                })
        
        return len(self.conflicts) == 0 and len(self.shortages) == 0
    
    def _get_eligible_staff(self, shift):
        eligible = []
        for staff in self.staff_list:
            if staff.get_role() == shift.get_required_role():
                eligible.append(staff)
        return eligible
    
    def _check_conflicts(self, staff, shift):
        if not staff.is_available_for_shift(shift.get_name()):
            return {
                'type': 'availability_mismatch',
                'staff': staff.get_name(),
                'shift': shift.get_name(),
                'message': f'{staff.get_name()} is not available for {shift.get_name()}'
            }
        
        if staff.is_already_assigned_to_shift(shift.get_name()):
            return {
                'type': 'double_booking',
                'staff': staff.get_name(),
                'shift': shift.get_name(),
                'message': f'{staff.get_name()} is already assigned to {shift.get_name()}'
            }
        
        return None
    
    def get_conflicts(self):
        return self.conflicts
    
    def get_shortages(self):
        return self.shortages
    
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
                print(f"  ⚠️  SHORTAGE: {shift.get_shortage()} staff needed")
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
