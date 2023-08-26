from rest_framework import generics,status
from .models import Timesheet,WeeklyTimesheet
from .serializers import TimeSheetSerializer,WeeklyTimesheetSerializer,WeeklyTimesheetManagerSerializer
from rest_framework import permissions
from datetime import datetime, timedelta
from rest_framework.response import Response
from django.db import transaction
from .permissions import IsManager
from django.shortcuts import get_object_or_404
from Employees.models import Employee


def calculate_working_days():
    # Get the current date
    today = datetime.now()

    # Calculate the start date (Monday of the current week)
    start_date = today - timedelta(days=today.weekday())

    # Initialize a list to store working days
    working_days = []

    # Determine the end date (Friday) by adding 4 days to the start_date
    end_date = start_date + timedelta(days=4)

    # Iterate through the days of the week
    current_date = start_date
    while current_date <= end_date:
        # Check if the current day is a weekday (0 = Monday, 4 = Friday)
        if current_date.weekday() < 5:  # Monday to Friday
            working_days.append(current_date.date())

        # Move to the next day
        current_date += timedelta(days=1)

    return working_days

class TimeSheetListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TimeSheetSerializer

    def get_queryset(self):
        # Filter timesheet entries based on the logged-in user's employee ID
        employee_id = self.request.user.employee_id
        return Timesheet.objects.filter(employee__employee_id=employee_id)

    def perform_create(self, serializer):
        # Automatically set the employee based on the logged-in user
        serializer.save(employee_id=self.request.user.employee_id)

# class TimeSheetCreateView(generics.CreateAPIView):
#     serializer_class = TimeSheetSerializer

#     def perform_create(self, serializer):
#         # Get the logged-in user's employee ID
#         employee_id = self.request.user.employee_id

#         # Set the 'employee' field of the timesheet to the logged-in user's employee ID
#         serializer.save(employee_id=employee_id)
        
class TimeSheetCreateView(generics.CreateAPIView):
    queryset = Timesheet.objects.all()
    serializer_class = TimeSheetSerializer
    permission_classes = [permissions.IsAuthenticated]  # Ensure user is authenticated

    def perform_create(self, serializer):
        # Get the currently logged-in employee
        logged_in_employee = self.request.user

        # Set the employee field of the timesheet to the logged-in employee
        serializer.save(employee=logged_in_employee)

class TimeSheetRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Timesheet.objects.all()
    serializer_class = TimeSheetSerializer

class TimeSheetRetrieveView(generics.RetrieveAPIView):
    queryset = Timesheet.objects.all()
    serializer_class = TimeSheetSerializer
    lookup_field = 'timesheet_id'
    
class TimeSheetListView(generics.ListAPIView):
    serializer_class = TimeSheetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Get the currently logged-in user
        user = self.request.user

        # Check if the user has the 'Manager' role
        if 'Manager' in user.role:  # Assuming 'role' is a list of roles
            # If the user is a manager, return all timesheets
            queryset = Timesheet.objects.all()
        else:
            # If the user is not a manager, filter timesheets by their employee
            queryset = Timesheet.objects.filter(employee=user)

        return queryset

class WeeklyTimesheetCreateView(generics.CreateAPIView):
    serializer_class = WeeklyTimesheetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        
        data = request.data.copy()
        data['employee'] = request.user.employee_id
        serializer = WeeklyTimesheetSerializer(data=data)
        if serializer.is_valid():
            # Automatically set the employee based on the logged-in user
            serializer.save(employee=request.user)
            return Response({'message': 'Timesheet submitted successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WeeklyTimesheetApproveView(generics.UpdateAPIView):
    queryset = WeeklyTimesheet.objects.all()
    serializer_class = WeeklyTimesheetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Check if the user is a manager (assuming "role" is a field in the Employee model)
        if request.user.role == 'Manager':
            instance.is_approved = True
            instance.approved_by = request.user
            instance.save()
            return Response({'message': 'Timesheet approved successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'You do not have permission to approve timesheets'}, status=status.HTTP_403_FORBIDDEN)

class WeeklyTimesheetListView(generics.ListAPIView):
    serializer_class = WeeklyTimesheetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Manager':
            # Managers can see all timesheets
            return WeeklyTimesheet.objects.all()
        else:
            # Employees can see only their own timesheets
            return WeeklyTimesheet.objects.filter(employee=user)

class WeeklyTimesheetManagerView(generics.ListAPIView):
    serializer_class = WeeklyTimesheetManagerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Assuming that managers are identified by their role
        if self.request.user.role == 'Manager':
            return WeeklyTimesheet.objects.all()
        else:
            return WeeklyTimesheet.objects.none()

    def post(self, request, *args, **kwargs):
        # Check if the user is a manager
        if request.user.role != 'Manager':
            return Response({'message': 'Only managers can approve time sheets.'}, status=status.HTTP_403_FORBIDDEN)

        timesheet_id = request.data.get('timesheet_id')
        try:
            timesheet = WeeklyTimesheet.objects.get(timesheet_id=timesheet_id)
        except WeeklyTimesheet.DoesNotExist:
            return Response({'message': 'Time sheet not found.'}, status=status.HTTP_404_NOT_FOUND)

        timesheet.is_approved = True
        timesheet.approved_by = request.user
        timesheet.save()

        return Response({'message': 'Time sheet approved successfully.'}, status=status.HTTP_200_OK)

class WeeklyTimesheetManagerListView(generics.ListAPIView):
    serializer_class = WeeklyTimesheetManagerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Get the employee_id from the URL
        employee_id = self.kwargs['employee_id']

        # Check if the user is a manager
        if self.request.user.role == 'Manager':
            return WeeklyTimesheet.objects.filter(employee__employee_id=employee_id)
        else:
            return WeeklyTimesheet.objects.none()
        
        
# class WeeklyTimesheetManagerDetailView(generics.RetrieveAPIView):
#     serializer_class = WeeklyTimesheetManagerSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         # Get the employee_id and timesheet_id from the URL
#         timesheet_id = self.kwargs['pk']

#         # Check if the user is a manager
#         if self.request.user.role == 'Manager':
#             return WeeklyTimesheet.objects.filter(timesheet_id=timesheet_id)
#         else:
#             return WeeklyTimesheet.objects.none()

#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()

#         if instance.is_approved:
#             return Response({'message': 'This time sheet is already approved.'}, status=status.HTTP_400_BAD_REQUEST)

#         serializer = self.get_serializer(instance)
#         return Response(serializer.data)

#     def put(self, request, *args, **kwargs):
#         instance = self.get_object()

#         if instance.is_approved:
#             return Response({'message': 'This time sheet is already approved.'}, status=status.HTTP_400_BAD_REQUEST)

#         # Check if the user is a manager
#         if request.user.role != 'Manager':
#             return Response({'message': 'Only managers can approve time sheets.'}, status=status.HTTP_403_FORBIDDEN)

#         instance.is_approved = True
#         instance.approved_by = request.user
#         instance.save()

#         return Response({'message': 'Time sheet approved successfully.'}, status=status.HTTP_200_OK)

class WeeklyTimesheetManagerDetailView(generics.RetrieveAPIView):
    serializer_class = WeeklyTimesheetManagerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Get the timesheet_id from the URL
        timesheet_id = self.kwargs['pk']

        # Check if the user is a manager
        if self.request.user.role == 'Manager':
            return WeeklyTimesheet.objects.filter(timesheet_id=timesheet_id)
        else:
            return WeeklyTimesheet.objects.none()

    def put(self, request, *args, **kwargs):
        instance = self.get_object()

        # Check if the user is a manager
        if request.user.role != 'Manager':
            return Response({'message': 'Only managers can approve time sheets.'}, status=status.HTTP_403_FORBIDDEN)

        # Check if the 'approve' field is in the request data
        if 'is_approved' in request.data and request.data['is_approved'] == 'true':
            # Set 'is_approved' to True
            instance.is_approved = True

            # Set 'approved_by' to the logged-in employee
            #instance.approved_by = request.user.employee_name
            employee_instance = get_object_or_404(Employee, employee_id=request.user)

            # Set 'approved_by' to the Employee instance
            instance.approved_by = employee_instance

            instance.save()

            return Response({'message': 'Time sheet approved successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'The "approve" field must be included in the request data and set to "true" to approve the time sheet.'}, status=status.HTTP_400_BAD_REQUEST)







