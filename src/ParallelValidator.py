from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from typing import List

class ParallelValidator:
    
    def __init__(self, max_workers=None):
        self.max_workers = max_workers
        self.stats = {'total': 0, 'parallel': 0}
    
    def validate_staff(self, staff_list: List, shift) -> dict:
        """Validate multiple staff availability for a shift."""
        self.stats['total'] += 1
        start_time = time.time()
        
        if len(staff_list) > 5:
            self.stats['parallel'] += 1
            results = self._parallel_validation(staff_list, shift)
        else:
            results = self._sequential_validation(staff_list, shift)
        
        return {
            'eligible': results['eligible'],
            'conflicts': results['conflicts'],
            'time': time.time() - start_time
        }
    
    def _parallel_validation(self, staff_list: List, shift) -> dict:

        """Parallel validation using ThreadPoolExecutor."""
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
    
    def _sequential_validation(self, staff_list: List, shift) -> dict:
        """Fallback for small lists"""
        eligible, conflicts = [], []
        
        for staff in staff_list:
            result = self._validate_single(staff, shift)
            if result['is_eligible']:
                eligible.append(staff)
            if result['conflict']:
                conflicts.append(result['conflict'])
        
        return {'eligible': eligible, 'conflicts': conflicts}
    
    def _validate_single(self, staff, shift) -> dict:
        """For 1 staff member on shift."""
        if staff.get_role() != shift.get_required_role():
            return {'is_eligible': False, 'conflict': {'type': 'role_mismatch'}}
        
        if not staff.is_available_for_shift(shift.get_name()):
            return {'is_eligible': False, 'conflict': {'type': 'availability'}}
        
        if staff.is_already_assigned_to_shift(shift.get_name()):
            return {'is_eligible': False, 'conflict': {'type': 'double_booking'}}
        
        return {'is_eligible': True, 'conflict': None}
    
    def get_statistics(self) -> dict:
        """Get validation performance statistics."""
        return {
            'total': self.stats['total'],
            'parallel': self.stats['parallel'],
            'sequential': self.stats['total'] - self.stats['parallel']
        }