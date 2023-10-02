from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.http import JsonResponse

class EmployeeManager(BaseUserManager):
    def create_user(self, employee_id, password=None, role=None, **extra_fields):
        if not employee_id:
            raise ValueError('The Employee ID field must be set')
        
        # Check if the role is "Manager" and set is_superuser accordingly
        is_superuser = extra_fields.pop('is_superuser', False)
        if role == 'Management':
            is_superuser = True
        
        # Create an instance of the Employee model with the provided data
        employee = self.model(employee_id=employee_id, role=role, **extra_fields)
        employee.set_password(password)
        employee.is_superuser = is_superuser
        employee.save(using=self._db)
        return employee

    def create_superuser(self, employee_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(employee_id, password, **extra_fields)


class Employee(AbstractBaseUser, PermissionsMixin):
    
    DEPARTMENT_CHOICES = [
        ('Management',"Management"),
        ('Human Resources', 'Human Resources'),
        ('Information Technology', 'Information Technology'),
        ('Finance', 'Finance'),
        ('Marketing', 'Marketing'),]
    
    employee_name = models.CharField(max_length=100)
    phonenumber = models.CharField(max_length=20,unique= True)
    employee_id = models.CharField(unique=True, max_length=10,primary_key=True)
    role = models.CharField(max_length=100,choices=DEPARTMENT_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = EmployeeManager()

    USERNAME_FIELD = 'employee_id'
    REQUIRED_FIELDS = ['employee_name', 'phonenumber', 'role']

    def __str__(self):
        return self.employee_id


