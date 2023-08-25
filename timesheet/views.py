from rest_framework import generics
from .models import Timesheet
from .serializers import TimeSheetSerializer
from rest_framework import permissions

class TimeSheetListCreateView(generics.ListCreateAPIView):
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







