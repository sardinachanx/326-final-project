from collections import OrderedDict
import datetime
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Course, Assignment, Enrollment, DayEntry, Student

# Helper methods/fields

User = get_user_model()

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

# Serializers

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
    day_entries = DayEntrySerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['url', 'email', 'name', 'username', 'password', 'profile', 'courses', 'day_entries']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self,validated_data):
        user = User.objects.create_user(name=validated_data['name'], email=validated_data['email'],
            username=validated_data['username'], password=validated_data['password'])
        return user


class AssignmentSerializer(serializers.ModelSerializer):
    avg_total_minutes = serializers.SerializerMethodField()
    avg_daily_minutes = serializers.SerializerMethodField()

    class Meta:
        model = Assignment
        fields = ['assigned_date', 'due_date', 'course', 'type', 'number', 'avg_total_minutes', 
            'avg_daily_minutes']
    
    def get_avg_total_minutes(self, obj):
        day_entries = obj.day_entries
        enrollment_size = obj.course.student.count()
        duration = timedelta(minutes=0)
        for day_entry in day_entries.all(): 
            duration += day_entry.duration
        return str(duration / enrollment_size)

    def get_avg_daily_minutes(self, obj):
        day_entries = obj.day_entries
        enrollment_size = obj.course.student.count()
        print(enrollment_size)
        duration_dict = {} 
        for day_entry in day_entries.all(): 
            day = day_entry.date
            if day not in duration_dict: 
                duration_dict[day] = day_entry.duration
            else: 
                duration_dict[day] += day_entry.duration
        date_range = duration_dict.keys()
        stringified_duration_dict = {}
        for day in daterange(min([min(date_range), obj.assigned_date]), max([max(date_range), obj.due_date])):
            if day not in duration_dict:
                stringified_duration_dict[str(day)] = timedelta(hours=0)
            else:
                stringified_duration_dict[str(day)] = str(duration_dict[day] / enrollment_size)
        return stringified_duration_dict
        


class CourseSerializer(serializers.ModelSerializer):
    assignments = AssignmentSerializer(many=True, read_only=True)
    

    class Meta:
        model = Course
        fields = ['url', 'name', 'id', 'subject',
                  'course_number', 'assignments']


class StatisticsSerializer(serializers.Serializer):
    total_minutes_this_week = serializers.SerializerMethodField()
    

    def get_total_minutes_this_week(self, obj):
        today = obj
        closest_sunday = today - datetime.timedelta(days=today.weekday())
        next_sunday = closest_sunday + datetime.timedelta(days=7)
        relevant_entries = self.context['request'].user.day_entries.filter(
            date__gte=closest_sunday, date__lte=next_sunday)
        # print(relevant_entries)
        total_hour_count = timedelta(0)
        for entry in relevant_entries: 
            total_hour_count += entry.duration
        return str(total_hour_count)
    
    

