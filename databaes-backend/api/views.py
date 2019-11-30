from django.contrib.auth import authenticate, login
from django.shortcuts import render
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response

from .models import Assignment, Course, DayEntry, Enrollment, User
from .serializers import (AssignmentSerializer, CourseSerializer,
                          DayEntrySerializer, EnrollmentSerializer,
                          TokenSerializer, UserSerializer)

# Create your views here.


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer


class DayEntryViewSet(viewsets.ModelViewSet):
    queryset = DayEntry.objects.all()
    serializer_class = DayEntrySerializer


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
