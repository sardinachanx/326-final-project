from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Course, Assignment, Enrollment, DayEntry, Student

User = get_user_model()

class EnrollmentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault().profile)

    class Meta:
        model = Enrollment
        fields = ['course', 'term', 'year', 'user']
        # extra_kwargs = {
        #     'course': {'write_only': True},
        #     'term': {'write_only': True},
        #     'year': {'write_only': True}
        # }
    


class DayEntrySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault().profile)

    class Meta:
        model = DayEntry
        fields = ['assignment', 'date', 'duration', 'user']


class StudentSerializer(serializers.ModelSerializer): 
    # courses = EnrollmentSerializer(source="enrollment_set", many=True, read_only=True)
    # day_entries = DayEntrySerializer(many=True, read_only=True)
    class Meta:
        model = Student
        fields = []


class UserSerializer(serializers.ModelSerializer):
    profile = StudentSerializer(required=False, read_only=True)

    class Meta:
        model = User
        fields = ['url', 'email', 'name', 'username', 'password', 'profile']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self,validated_data):
        user = User.objects.create_user(name=validated_data['name'], email=validated_data['email'],
            username=validated_data['username'], password=validated_data['password'])
        return user


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['assigned_date', 'due_date', 'course', 'type', 'number']


class CourseSerializer(serializers.ModelSerializer):
    assignments = AssignmentSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['url', 'name', 'id', 'subject',
                  'course_number', 'assignments']

