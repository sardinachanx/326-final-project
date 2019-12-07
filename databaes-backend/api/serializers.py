from collections import OrderedDict
import datetime
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Course, Assignment, Enrollment, DayEntry, Student

# Helper methods/fields

User = get_user_model()

def daterange(start_date, end_date, skip=1):
    for n in range(0, int ((end_date - start_date).days), skip):
        yield start_date + timedelta(n)

def get_week(target_date):
    closest_sunday = target_date - timedelta(days=target_date.weekday())
    next_saturday = closest_sunday + timedelta(days=6)
    return (closest_sunday, next_saturday)

# Serializers

class EnrollmentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    course_name = serializers.SerializerMethodField()

    class Meta:
        model = Enrollment
        fields = ['course_name', 'course', 'term', 'year', 'user']
        # extra_kwargs = {
        #     'course': {'write_only': True},
        # }

    def get_course_name(self, obj):
        return obj.course.__str__()
    


class DayEntrySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = DayEntry
        fields = ['assignment', 'date', 'duration', 'user']


class SimplifiedAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id', 'assigned_date', 'due_date', 'type', 'number']



class AssignmentSerializer(SimplifiedAssignmentSerializer):
    avg_total_hours = serializers.SerializerMethodField()
    avg_daily_hours = serializers.SerializerMethodField()

    class Meta:
        model = Assignment
        fields = SimplifiedAssignmentSerializer.Meta.fields + ['course', 'avg_total_hours', 'avg_daily_hours']
    
    def get_avg_total_hours(self, obj):
        day_entries = obj.day_entries
        enrollment_size = obj.course.student.count()
        duration = timedelta(minutes=0)
        for day_entry in day_entries.all(): 
            duration += day_entry.duration
        return str(duration / enrollment_size)

    def get_avg_daily_hours(self, obj):
        day_entries = obj.day_entries
        enrollment_size = obj.course.student.count()

        duration_dict = {} 
        for day_entry in day_entries.all(): 
            day = day_entry.date
            if day not in duration_dict: 
                duration_dict[day] = day_entry.duration
            else: 
                duration_dict[day] += day_entry.duration
        date_range = duration_dict.keys()
        stringified_duration_dict = {}
        for day in daterange(min([min(date_range, default=obj.assigned_date), obj.assigned_date]), 
                                max([max(date_range, default=obj.due_date), obj.due_date]) + timedelta(1)):
            if day not in duration_dict:
                stringified_duration_dict[str(day)] = timedelta(hours=0)
            else:
                stringified_duration_dict[str(day)] = str(duration_dict[day] / enrollment_size)
        return stringified_duration_dict
        

class SimplifiedCourseSerializer(serializers.ModelSerializer):
    average_weekly_hours = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'subject', 'course_number', 'name', 'average_weekly_hours']

    def get_average_weekly_hours(self, obj):
        total_list = [entry for assignment in obj.assignments.all() for entry in assignment.day_entries.all()]
        print(total_list)
        if len(total_list) == 0:
            return str(timedelta(hours=0))
        enrollment_size = obj.student.count()
        start_date = min(total_list, key=(lambda x: x.date)).date
        end_date = max(total_list, key=(lambda x: x.date)).date
        num_weeks = ((end_date - start_date).days + 1) / 7 
        print(num_weeks)
        return str(sum((entry.duration for entry in total_list), timedelta()) / num_weeks / enrollment_size)


class CourseSerializer(SimplifiedCourseSerializer):
    assignments = SimplifiedAssignmentSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = SimplifiedCourseSerializer.Meta.fields + ['assignments']


class StatisticsSerializer(serializers.Serializer):
    # weekly_total_minutes_by_day = serializers.SerializerMethodField()
    # total_minutes_by_week = serializers.SerializerMethodField()
    user_stats = serializers.SerializerMethodField() 

    def get_user_stats(self, obj): 
        result_dict = {} 
        user_day_entries = self.context['request'].user.day_entries.all()
        result_dict['total_hours_by_week'] = self.get_total_hours_by_week(obj, user_day_entries)
        result_dict['weekly_total_hours_by_day'] = self.get_weekly_total_hours_by_day(obj, user_day_entries)
        result_dict['course_breakdown'] = self.get_course_stats(obj, user_day_entries)
        return result_dict

    
    def get_total_hours_by_week(self, obj, db):
        page_length = self.context['pages']
        last_date = obj 
        weekly_buckets = {}
        for _ in range(page_length):
            closest_sunday, next_saturday = get_week(last_date)
            relevant_entries = db.filter(
                date__gte=closest_sunday, date__lte=next_saturday)
            weekly_buckets[str(closest_sunday)] = str(sum((entry.duration for entry in relevant_entries), 
                timedelta()))
            last_date = closest_sunday - timedelta(days=1)
        return weekly_buckets

    def get_weekly_total_hours_by_day(self, obj, db):
        last_date = obj
        daily_bucket = {}
        closest_sunday, next_saturday = get_week(last_date)
        relevant_entries = db.filter(
            date__gte=closest_sunday, date__lte=next_saturday)
        for entry in relevant_entries: 
            if entry.date not in daily_bucket:
                daily_bucket[date] = entry.duration
            else:
                daily_bucket[date] += entry.duration
        stringified_daily_bucket = {}
        for cday in daterange(closest_sunday, closest_sunday + timedelta(7)):
            if cday not in daily_bucket: 
                stringified_daily_bucket[str(cday)] = str(timedelta(hours=0))
            else:
                stringified_daily_bucket[str(cday)] = str(daily_bucket[cday])
        return stringified_daily_bucket

    def get_course_stats(self, obj, db): 
        bucket = {}
        draft = {}
        for entry in db: 
            course_id = entry.assignment.course.id
            assignment_id = entry.assignment.id
            if course_id not in bucket: 
                bucket[course_id] = {} 
                draft[course_id] = {}
            if assignment_id not in bucket[course_id]:
                bucket[course_id][assignment_id] = timedelta(hours=0)
                draft[course_id][assignment_id] = {'min': None, 'max': None}
            bucket[entry.assignment.course.id][entry.assignment.id] += entry.duration 
            if not draft[course_id][assignment_id]['min'] or entry.date < draft[course_id][assignment_id]['min']:
                draft[course_id][assignment_id]['min'] = entry.date
            if not draft[course_id][assignment_id]['max'] or entry.date > draft[course_id][assignment_id]['max']: 
                draft[course_id][assignment_id]['max'] = entry.date
        print(bucket)
        print(draft)
        final_bucket = {} 
        for (course, info) in bucket.items(): 
            final_bucket[course] = {'average_hours_per_week': timedelta(0), 'assignment_breakdown': {}}
            for (assignment, duration) in info.items(): 
                avg_hours = duration / ((draft[course][assignment]['max'] - draft[course][assignment]['min'] + \
                            timedelta(days=1)).days / 7)
                final_bucket[course]['assignment_breakdown'] = {
                    assignment:{
                        'total_hours': str(duration),
                        'avg_hours': str(avg_hours)
                    }
                }
                final_bucket[course]['average_hours_per_week'] += avg_hours
            final_bucket[course]['average_hours_per_week'] = str(final_bucket[course]['average_hours_per_week'])
        return final_bucket

        

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
