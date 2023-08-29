from django.conf import settings
from django.db import models
from Employees.models import Employee
from django.core.exceptions import ValidationError

class Timesheet(models.Model):
    employee = models.ForeignKey(Employee,
        on_delete=models.CASCADE)
    timesheet_id = models.CharField(max_length=20, primary_key=True, editable=False, unique=True)

    def save(self, *args, **kwargs):
        # Generate the custom primary key: Employee_id + date (in a specific format)
        self.timesheet_id = f"{self.employee.employee_id}_{self.date.strftime('%Y%m%d')}"

        super().save(*args, **kwargs)
    
    date = models.DateField()
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField(blank=True)
    Day_type = [
        ('working', 'Working'),
        ('sickleave', 'Sick Leave'),
        ('personalleave', 'Personal Leave'),
        ('holiday', 'Holiday'),
        ('projectholiday', 'Project Holiday'),
    ]
    day_type = models.CharField(max_length=15, choices=Day_type, default=Day_type[0])
    

    # def __str__(self):
    #     return f"{self.employee.employee_id} - {self.date}"
    def __str__(self):
        return self.timesheet_id
    
    
class WeeklyTimesheet(models.Model):
    # ForeignKey to associate the timesheet with an employee
    
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='timesheets_submitted'  # Custom related name for submitted timesheets
    )
    
    # Dates for the five working days of a week
    date1 = models.DateField()
    date2 = models.DateField()
    date3 = models.DateField()
    date4 = models.DateField()
    date5 = models.DateField()
    
    # Hours worked for each day
    hours_worked1 = models.DecimalField(max_digits=5, decimal_places=2)
    hours_worked2 = models.DecimalField(max_digits=5, decimal_places=2)
    hours_worked3 = models.DecimalField(max_digits=5, decimal_places=2)
    hours_worked4 = models.DecimalField(max_digits=5, decimal_places=2)
    hours_worked5 = models.DecimalField(max_digits=5, decimal_places=2)
    
    # Descriptions for each day (optional)
    description1 = models.TextField(blank=True)
    description2 = models.TextField(blank=True)
    description3 = models.TextField(blank=True)
    description4 = models.TextField(blank=True)
    description5 = models.TextField(blank=True)
    
    # Choices for the type of day (working, sick leave, etc.) for each day
    DAY_TYPE_CHOICES = [
        ('working', 'Working'),
        ('sickleave', 'Sick Leave'),
        ('personalleave', 'Personal Leave'),
        ('holiday', 'Holiday'),
        ('projectholiday', 'Project Holiday'),
    ]
    
    # Fields to store the type of day for each day
    day_type1 = models.CharField(max_length=15, choices=DAY_TYPE_CHOICES, default='working')
    day_type2 = models.CharField(max_length=15, choices=DAY_TYPE_CHOICES, default='working')
    day_type3 = models.CharField(max_length=15, choices=DAY_TYPE_CHOICES, default='working')
    day_type4 = models.CharField(max_length=15, choices=DAY_TYPE_CHOICES, default='working')
    day_type5 = models.CharField(max_length=15, choices=DAY_TYPE_CHOICES, default='working')
    
    timesheet_id = models.CharField(max_length=20, primary_key=True, editable=False, unique=True)
    
    is_approved = models.BooleanField(default=False)

    # Manager who approved the timesheet (ForeignKey to Employee)

    approved_by = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='timesheets_approved'  # Custom related name for approved timesheets
    )
    
    def clean(self):
        # Check if the dates are unique
        dates = [self.date1, self.date2, self.date3, self.date4, self.date5]
        if len(dates) != len(set(dates)):
            raise ValidationError('Dates must be unique within the same timesheet.')

    def save(self, *args, **kwargs):
        # Generate the custom primary key: Employee_id + date (in a specific format)
        # For this example, let's use date1 as the date for timesheet_id
        self.timesheet_id = f"{self.employee.employee_id}_{self.date1.strftime('%Y%m%d')}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.timesheet_id