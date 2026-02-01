import csv
import random
from faker import Faker
from datetime import datetime, timedelta

def generate_roster():
    fake = Faker()
    
    roles = ['Analyst', 'Manager', 'Director', 'VP']
    departments = ['Sales', 'Engineering', 'G&A']
    
    salary_ranges = {
        'Analyst': (70000, 90000),
        'Manager': (110000, 150000),
        'Director': (160000, 200000),
        'VP': (220000, 280000)
    }
    
    roster_file = 'current_roster.csv'
    
    with open(roster_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Employee_ID', 'Name', 'Role', 'Department', 'Base_Salary', 'Start_Date'])
        
        for i in range(50):
            emp_id = 1000 + i + 1
            name = fake.name()
            role = random.choice(roles)
            department = random.choice(departments)
            
            # Generate salary based on role
            min_sal, max_sal = salary_ranges[role]
            salary = random.randint(min_sal, max_sal)
            
            # Generate start date within last 3 years
            start_date = fake.date_between(start_date='-3y', end_date='today')
            
            writer.writerow([emp_id, name, role, department, salary, start_date])
            
    print('Roster generation complete')

if __name__ == "__main__":
    generate_roster()
