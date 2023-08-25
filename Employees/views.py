from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import Employee
from .serializers import EmployeeRegistrationSerializer, LoginSerializer,EmployeeSerializer,PasswordChangeSerializer,ProfileUpdateSerializer
from rest_framework.permissions import AllowAny,IsAuthenticated, IsAdminUser
from django.contrib.auth.decorators import login_required


class EmployeeRegistrationView(generics.CreateAPIView):
    serializer_class = EmployeeRegistrationSerializer
    permission_classes = [permissions.AllowAny]  # Allow unauthenticated users to register

    def perform_create(self, serializer):
        user = serializer.save()
        return user

class LoginView(APIView):
    authentication_classes = []  # Remove authentication classes for this view
    permission_classes = [AllowAny]  # Use AllowAny permission to allow unauthenticated access

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            employee_id = validated_data.get('employee_id')
            password = validated_data.get('password')

            user = authenticate(request, employee_id=employee_id, password=password)

            if user is not None:
                refresh = RefreshToken.for_user(user)
                data = {
                    'refresh_token': str(refresh),
                    'access_token': str(refresh.access_token),
                }
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            access_token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        except Exception:
            return Response({'detail': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            RefreshToken(access_token).blacklist()
            return Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'detail': 'Failed to logout'}, status=status.HTTP_400_BAD_REQUEST)

class EmployeeDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]# Only authenticated users can access this view

    def get(self, request):
        user = request.user

        # Check if the user is a manager
        if user.role == 'Manager':
            employees = Employee.objects.all()
            serializer = EmployeeSerializer(employees, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # If the user is not a manager, they can only see their own details
        serializer = EmployeeSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

# @login_required(login_url='/login/')  # Redirect to the login page if not logged in
# def employee_detail(request):
#     user = request.user

#     # Check if the user is a manager
#     if user.role == 'Manager':
#         employees = Employee.objects.all()
#         serializer = EmployeeSerializer(employees, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     # If the user is not a manager, they can only see their own details
#     serializer = EmployeeSerializer(user)
#     return Response(serializer.data, status=status.HTTP_200_OK)

@login_required(login_url='/login')  # Redirect to the login page if not logged in
def employee_detail(request):
    user = request.user

    if user.role == 'Manager':
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
    else:
        # If the user is not a manager, they can only see their own details
        serializer = EmployeeSerializer(user)

    return Response(serializer.data, status=status.HTTP_200_OK)

class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data)

        if serializer.is_valid():
            current_password = serializer.validated_data.get('current_password')
            new_password = serializer.validated_data.get('new_password')
            user = request.user

            # Check if the current password is correct
            if user.check_password(current_password):
                # Update the user's password with the new one
                user.set_password(new_password)
                user.save()
                return Response({'detail': 'Password changed successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Current password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = ProfileUpdateSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Profile updated successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeDeletionView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]  # Ensure only managers can delete employees

    def delete(self, request, employee_id):
        try:
            employee = Employee.objects.get(employee_id=employee_id)
        except Employee.DoesNotExist:
            return Response({'detail': 'Employee not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user is an admin or manager (assuming managers have the 'Manager' role)
        if request.user.role != 'Manager':
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        # Delete the employee
        employee.delete()
        return Response({'detail': 'Employee deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)



