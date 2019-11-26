from django.shortcuts import render
from .models import User, Course, Assignment, DayEntry, Enrollment
from .serializers import CourseSerializer, AssignmentSerializer, DayEntrySerializer, EnrollmentSerializer, UserSerializer, TokenSerializer
from django.contrib.auth import authenticate, login
from rest_framework_jwt.settings import api_settings
from rest_framework.response import Response
from rest_framework import permissions, generics, viewsets, status

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


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

class LoginView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny, )
    queryset = User.objects.all() 
    
    def post(self, request, *args, **kwargs):
        email = request.data.get('email', '')
        password = request.data.get('password', '')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            serializer = TokenSerializer(data={
               'token': jwt_encode_handler(
                  jwt_payload_handler(user)
              )}
            )
            serializer.is_valid()
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

