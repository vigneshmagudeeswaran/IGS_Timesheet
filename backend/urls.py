from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import ( TokenObtainPairView, TokenRefreshView)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('Employees.urls')),
    path('api/timesheet/', include('timesheet.urls')),
    # path('auth/', include('rest_framework.urls')),
    path('api/token/access/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
