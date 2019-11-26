from rest_framework import serializers
from .models import Course, Assignment, User, Enrollment, DayEntry, Student


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

class DayEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = DayEntry
        fields = ['student', 'assignment', 'date', 'duration']
        extra_kwargs = {'student': {'write_only': True}}


class StudentSerializer(serializers.ModelSerializer):
    courses = serializers.StringRelatedField(
        many=True,
        read_only=True
    )
    day_entries = DayEntrySerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Student
        fields = ['courses', 'day_entries']


class UserSerializer(serializers.ModelSerializer):
    profile = StudentSerializer(required=False, read_only=True)

    class Meta:
        model = User
        fields = ['url', 'email', 'name', 'username', 'password', 'profile']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['assigned_date', 'due_date', 'course', 'type', 'number']


class CourseSerializer(serializers.ModelSerializer):
    assignments = AssignmentSerializer(many=True, read_only=True)
    class Meta:
        model = Course
        # depth = 2
        fields = ['name', 'subject', 'course_number', 'assignments']

class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255)

