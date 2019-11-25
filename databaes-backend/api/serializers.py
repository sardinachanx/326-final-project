from rest_framework import serializers
from .models import Course, Assignment, User, Enrollment, DayEntry, Student


class CourseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Course
        depth = 2
        fields = ['name', 'subject', 'course_number', 'assignments']


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['student', 'course', 'term', 'year']
        extra_kwargs = {
            'student': {'write_only': True}, 
            'course': {'write_only': True}, 
            'term': {'write_only': True}, 
            'year': {'write_only': True}
        }


class StudentSerializer(serializers.ModelSerializer):
    courses = serializers.StringRelatedField(
        many=True,
        read_only=True
    )

    class Meta:
        model = Student
        fields = ['courses']


class UserSerializer(serializers.ModelSerializer):
    profile = StudentSerializer(required=True)

    class Meta:
        model = User
        fields = ['url', 'email', 'name', 'username', 'password', 'profile']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        read_only_fields = ['profile']


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['assigned_date', 'due_date', 'course', 'type', 'number']


class DayEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = DayEntry
        fields = ['student', 'assignment', 'date', 'duration']
        extra_kwargs = {'student': {'write_only': True}}
