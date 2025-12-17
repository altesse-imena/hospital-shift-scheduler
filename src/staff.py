class Staff:
    def __init__(self, staff_id, name, role, available_shifts):
        self.id = staff_id
        self.name = name
        self.role = role
        self.available_shifts = available_shifts
        self.assigned_shifts = []
    
    def get_id(self):
        return self.id
    
    def get_name(self):
        return self.name
    
    def get_role(self):
        return self.role
    
    def get_available_shifts(self):
        return self.available_shifts
    
    def get_assigned_shifts(self):
        return self.assigned_shifts
    
    def add_assigned_shift(self, shift_name):
        self.assigned_shifts.append(shift_name)
    
    def get_assignment_count(self):
        return len(self.assigned_shifts)
    
    def is_available_for_shift(self, shift_name):
        return shift_name in self.available_shifts
    
    def is_already_assigned_to_shift(self, shift_name):
        return shift_name in self.assigned_shifts
