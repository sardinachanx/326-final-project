from rest_framework import serializers
from .models import Course, Assignment, User, Enrollment, DayEntry


class CourseSerializer(serializers.ModelSerializer):
    # assignments = ??? name + url
    class Meta:
        model = Course
        fields = ['subject', 'course_number', 'assignments']


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
    courses = CourseSerializer(source='enrollment', many=True, read_only=True)
    pass 


class UserSerializer(serializers.ModelSerializer):
    profile = StudentSerializer(required=True)

    class Meta:
        model = User
        fields = ['url', 'email', 'name', 'password', 'profile']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['assigned_date', 'due_date', 'course', 'type', 'number']


class DayEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = DayEntry
        fields = ['student', 'assignment', 'date', 'duration']
        extra_kwargs = {'student': {'write_only': True}}
