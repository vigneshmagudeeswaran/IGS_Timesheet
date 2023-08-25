from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import ( TokenObtainPairView, TokenRefreshView)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Employees.urls')),
    path('timesheet/', include('timesheet.urls')),
    path('auth/', include('rest_framework.urls')),
    path('token/access/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
