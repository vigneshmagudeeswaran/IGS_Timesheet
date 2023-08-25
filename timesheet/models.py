from django.conf import settings
from django.db import models
from Employees.models import Employee

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
