from django.db import models
from Employees.models import Employee


class MailChecker(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    is_data = models.BooleanField(default=False)
    


