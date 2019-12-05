import datetime
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Course, Assignment, Enrollment, DayEntry, Student

User = get_user_model()

class EnrollmentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    course_name = serializers.SerializerMethodField()

    class Meta:
        model = Enrollment
        fields = ['course_name', 'course', 'term', 'year', 'user']
        extra_kwargs = {
            'course': {'write_only': True},
        }

    def get_course_name(self, obj):
        return obj.course.__str__()
    


class DayEntrySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = DayEntry
        fields = ['assignment', 'date', 'duration', 'user']


class StudentSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Student
        fields = []


class UserSerializer(serializers.ModelSerializer):
    profile = StudentSerializer(required=False, read_only=True)
    courses = EnrollmentSerializer(source="enrollment_set", many=True, read_only=True)
    # day_entries = DayEntrySerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['url', 'email', 'name', 'username', 'password', 'profile', 'courses']
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


class StatisticsSerializer(serializers.Serializer):
    total_minutes_this_week = serializers.SerializerMethodField()

    def get_total_minutes_this_week(self, obj):
        today = date.today()
        closest_sunday = today - datetime.timedelta(days=today.weekday())
        relevant_entries = obj.day_entries.filter(date__gte=closest_sunday, date__lte=today)
        print(relevant_entries)
        total_hour_count = timedelta(0)
        for entry in relevant_entries: 
            total_hour_count += entry.duration
        return str(total_hour_count)

