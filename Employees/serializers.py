from rest_framework import serializers
from .models import Employee
from django.contrib.auth.hashers import make_password


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

        
# class EmployeeRegistrationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Employee
#         fields = ['employee_name', 'phonenumber', 'employee_id', 'role', 'password']
#         extra_kwargs = {'password': {'write_only': True}}

class EmployeeRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['employee_name', 'phonenumber', 'employee_id', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Hash the password before saving it
        validated_data['password'] = make_password(validated_data['password'])
        employee = Employee.objects.create(**validated_data)
        return employee

class LoginSerializer(serializers.Serializer):
    employee_id = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    
class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['employee_name', 'phonenumber'] 