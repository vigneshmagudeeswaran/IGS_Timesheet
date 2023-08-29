from django.urls import path
from .views import TimeSheetListCreateView, TimeSheetRetrieveUpdateDestroyView,TimeSheetCreateView,TimeSheetRetrieveView,TimeSheetListView,WeeklyTimesheetCreateView,WeeklyTimesheetApproveView,WeeklyTimesheetListView,WeeklyTimesheetManagerView,WeeklyTimesheetManagerDetailView

urlpatterns = [
    #path('', TimeSheetListCreateView.as_view(), name='timesheet-list-create'),
    path('<int:employee_id>/<int:pk>/', TimeSheetRetrieveUpdateDestroyView.as_view(), name='timesheet-retrieve-update-destroy'),
    path('create/', TimeSheetCreateView.as_view(), name='timesheet-create'),
    #path('<str:timesheet_id>/', TimeSheetRetrieveView.as_view(), name='timesheet-retrieve'),
    path('', TimeSheetListView.as_view(), name='timesheet-list'),
    path('weekly_timesheet_create/', WeeklyTimesheetCreateView.as_view(), name='weekly-timesheet'),
    path('timesheet_approval/<str:pk>', WeeklyTimesheetManagerDetailView.as_view(), name='weekly-timesheet'),
    path('weekly_timesheet/', WeeklyTimesheetListView.as_view(), name='list-timesheets'),
]
