from django.contrib import admin
from django.urls import path,include
from django.views.generic import TemplateView
# from .views import EmployeeList, EmployeeDetail
from .views import LoginView,LogoutView,EmployeeRegistrationView,EmployeeDetailView,PasswordChangeView,ProfileUpdateView,EmployeeDeletionView

urlpatterns = [
    path('register/', EmployeeRegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # path('<int:pk>/', EmployeeList.as_view(), name ='timesheetlistcreate'),
    path('employee_detail/', EmployeeDetailView.as_view(), name ='Employeedetail'),
    path('change-password/', PasswordChangeView.as_view(), name='change-password'),
    path('update-profile/', ProfileUpdateView.as_view(), name='update-profile'),
    path('delete-employee/<str:employee_id>/', EmployeeDeletionView.as_view(), name='delete-employee'),
]
