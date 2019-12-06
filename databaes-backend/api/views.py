from datetime import date

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.db.models.query import EmptyQuerySet
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.serializers import CurrentUserDefault, HiddenField
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Assignment, Course, DayEntry, Enrollment, Student, User
from .permissions import IsEnrollmentOwner, IsProfileOwner
from .serializers import (AssignmentSerializer, CourseSerializer, DayEntrySerializer,
                          EnrollmentSerializer, SimplifiedAssignmentSerializer,
                          SimplifiedCourseSerializer, StatisticsSerializer, UserSerializer)

# Create your views here.


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return SimplifiedCourseSerializer
        return CourseSerializer


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer


class DayEntryViewSet(viewsets.ModelViewSet):
    serializer_class = DayEntrySerializer

    def get_queryset(self):
        queryset = DayEntry.objects.all().filter(user=self.request.user)
        assignment_id = self.request.query_params.get('assignment_id', None)
        if assignment_id is not None: 
            queryset = queryset.filter(assignment__id=assignment_id)
        return queryset


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    # Intended permissions:
    # Enroll, unenroll, or update enrollment: User only/Admin
    # View all enrollment: Admin only
    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [IsEnrollmentOwner]
        elif self.action == 'list':
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Intended permissions:
    # Get, update, or delete particular user: User only/Admin
    # List all users: Admin only
    # Create new user (register): Unrestricted
    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [IsProfileOwner]
        elif self.action == 'list':
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def get_object(self):
        if self.request.user.is_authenticated and self.kwargs['pk'] == 'me':
            return self.request.user
        else:
            return super().get_object()


class StatisticsViewSet(viewsets.ViewSet):
    queryset = Student.objects.none()
    serializer_class = StatisticsSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def list(self, request):
        d = request.query_params.get('date', None)
        interval = request.query_params.get('pages', 4)
        if d is None: 
            d = date.today()
        s = StatisticsSerializer(instance=d, context={'request': request, 'pages': interval})
        return Response(s.data)
