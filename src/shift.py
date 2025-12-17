class Shift:
    def __init__(self, name, required_role, required_count=1):
        self.name = name
        self.required_role = required_role
        self.required_count = required_count
        self.assigned_staff = []
    
    def get_name(self):
        return self.name
    
    def get_required_role(self):
        return self.required_role
    
    def get_required_count(self):
        return self.required_count
    
    def get_assigned_staff(self):
        return self.assigned_staff
    
    def add_staff(self, staff):
        self.assigned_staff.append(staff)
    
    def is_fully_staffed(self):
        return len(self.assigned_staff) >= self.required_count
    
    def get_shortage(self):
        return max(0, self.required_count - len(self.assigned_staff))
