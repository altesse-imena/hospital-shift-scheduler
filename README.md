# Hospital Shift Scheduling Engine

## Overview

A scheduling engine that assigns medical staff to shifts while respecting availability.

---

## Project Scope

We need a program that shows:

- **Employee Types**: Part-time and Full-time employees
- **Departments**: Payroll, Staff, Administration, IT  
- **Roles**: Hierarchies per department
- **Management Structure**: Employee-to-manager reporting relationships

### Key Requirements

- Assign shifts fairly
- Detect conflicts and shortages
- Parallelize availability validation
- Handle invalid schedules and missing staff

### Technical Requirements

1. **Object-Oriented Programming (OOP)**
   - Inheritance hierarchies
   - Encapsulation of employee data
   - Abstraction for common behaviors
   - Polymorphism for position-specific actions

2. **Binding Demonstrations**
   - Dynamic binding using method overriding
   - Static binding using method overloading

3. **Exception Handling**
   - Custom exception classes for invalid data
   - Comprehensive error coverage

4. **Parallel Programming**
   - Parallel data validation
   - Concurrent processing of requests

---

## Sys Architecture

### Class Structure

1. **main.py**
    -Entry & Init

2. **Staff.py**
    -ID
    -Name
    -Role
    -Availability
    -Assignments

3. **Shift.py**
    -Name
    -Required Count
    -Required Role
    -Assigned Staff
    -Shortage
4. **ScheduleManager.py**
    -Assign Shifts
    -Check Conflicts
    -Detect Shortages
    -Print Schedules
---

### Data Flow

1. **Init**: Load staff and shift data
2. **Eligibility Filtering**: Find staff matching shift role requirements
3. **Availability Validation**: Check if staff are available for the shift
4. **Conflict Detection**: Ensure no double-booking or violations
5. **Assignment**: Assign staff to shifts fairly
6. **Reporting**: Display schedule, conflicts, and shortages

---

## Setup

### Prerequisites
- Python 3.8 or higher
- No external dependencies required (uses standard library)

### Installation

```bash
# Clone the repository
git clone <https://github.com/altesse-imena/hospital-shift-scheduler.git>
cd hospital-shift-scheduler

# No pip install - uses only standard lib
```

---

## Running App

### Basic Execution

```bash
python main.py
```

### Expected Output

```
Hospital Shift Scheduling Engine
==================================================

Loaded 5 staff members
Loaded 7 shifts

Attempting to assign shifts...

✓ Scheduling completed successfully!

=== SHIFT SCHEDULE ===

Shift: Morning (Role: Doctor)
  Required: 1
  Assigned Staff:
    - Dr. Smith (ID: 1)

Shift: Morning (Role: Nurse)
  Required: 2
  Assigned Staff:
    - Nurse Williams (ID: 3)
    - Nurse Davis (ID: 5)

...
```

### Handling Errors

If scheduling fails, you'll see:

```
✗ Scheduling failed with errors:

CONFLICTS DETECTED:
  - Dr. Smith is not available for Afternoon

STAFF SHORTAGES:
  - Shift 'Night' needs 1 more Doctor(s)
```

---

