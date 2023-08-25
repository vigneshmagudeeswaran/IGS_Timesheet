from django.urls import path
from .views import TimeSheetListCreateView, TimeSheetRetrieveUpdateDestroyView,TimeSheetCreateView,TimeSheetRetrieveView,TimeSheetListView

urlpatterns = [
    #path('', TimeSheetListCreateView.as_view(), name='timesheet-list-create'),
    path('<int:employee_id>/<int:pk>/', TimeSheetRetrieveUpdateDestroyView.as_view(), name='timesheet-retrieve-update-destroy'),
    path('create/', TimeSheetCreateView.as_view(), name='timesheet-create'),
    path('<str:timesheet_id>/', TimeSheetRetrieveView.as_view(), name='timesheet-retrieve'),
    path('', TimeSheetListView.as_view(), name='timesheet-list'),
]