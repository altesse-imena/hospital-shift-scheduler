from staff import Staff
from shift import Shift
from schedule_manager import ScheduleManager
from ScheduleExceptions import SchedulingException 

def load_sample_data():
    staff_list = [
        Staff(1, "Dr. Smith", "Doctor", ["Morning", "Evening"]),
        Staff(2, "Dr. Johnson", "Doctor", ["Morning", "Night"]),
        Staff(3, "Nurse Williams", "Nurse", ["Morning", "Afternoon", "Evening"]),
        Staff(4, "Nurse Brown", "Nurse", ["Afternoon", "Night"]),
        Staff(5, "Nurse Davis", "Nurse", ["Morning", "Evening", "Night"]),
    ]
    
    shift_list = [
        Shift("Morning", "Doctor", 1),
        Shift("Morning", "Nurse", 2),
        Shift("Afternoon", "Nurse", 1),
        Shift("Evening", "Doctor", 1),
        Shift("Evening", "Nurse", 1),
        Shift("Night", "Doctor", 1),
        Shift("Night", "Nurse", 1),
    ]
    
    return staff_list, shift_list


def main():
    print("Hospital Shift Scheduling Engine")
    print("=" * 50)
    
    staff_list, shift_list = load_sample_data()
    
    print(f"\nLoaded {len(staff_list)} staff members")
    print(f"Loaded {len(shift_list)} shifts")
    
    manager = ScheduleManager(staff_list, shift_list)
    
    print("\nAttempting to assign shifts...")
    
    try:
        success = manager.assign_shifts()
        
        if success:
            print("\n✓ Scheduling completed successfully!\n")
            manager.print_schedule()
            manager.print_staff_assignments()
        else:
            print("\n✗ Scheduling failed with errors:\n")
            
            conflicts = manager.get_conflicts()
            if conflicts:
                print("CONFLICTS DETECTED:")
                for conflict in conflicts:
                    print(f"  - {conflict['message']}")
                print()
            
            shortages = manager.get_shortages()
            if shortages:
                print("STAFF SHORTAGES:")
                for shortage in shortages:
                    print(f"  - Shift '{shortage['shift']}' needs {shortage['shortage']} more {shortage['required_role']}(s)")
                print()
            
            print("Partial schedule (where possible):")
            manager.print_schedule()
            manager.print_staff_assignments()
            
            # Show validation statistics
            stats = manager.validator.get_statistics()
            print(f"\nValidation Statistics:")
            print(f"  Total validations: {stats['total']}")
            print(f"  Parallel validations: {stats['parallel']}")
            print(f"  Sequential validations: {stats['sequential']}")
    
    except SchedulingException as e:
        print(f"\n✗ Scheduling failed with error: {e}")
        print(f"  Context: {e.context if hasattr(e, 'context') else 'None'}")
    except Exception as e:
        print(f"\n✗ Unexpected error: {str(e)}")
    
    # Print any errors collected during scheduling
    errors = manager.get_errors()
    if errors:
        print(f"\n✗  {len(errors)} error(s) occurred during scheduling:")
        for error in errors:
            if isinstance(error, SchedulingException):
                print(f"  - {error.error_code}: {error.message}")
            else:
                print(f"  - {error}")

if __name__ == "__main__":
    main()