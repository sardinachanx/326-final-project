"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from api import views

# Create router
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'courses', views.CourseViewSet)
router.register(r'assignments', views.AssignmentViewSet)
router.register(r'day-entries', views.DayEntryViewSet)
router.register(r'enrollment', views.EnrollmentViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/login/', TokenObtainPairView.as_view(), name='token-login'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('api-auth/', include('rest_framework.urls')),
]
