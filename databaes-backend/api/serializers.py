from rest_framework import serializers
from .models import Course, Assignment, User, Enrollment, DayEntry, Student


class EnrollmentSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(
    #     required=False,
    #     read_only=True,
    #     default=serializers.CurrentUserDefault
    # )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Enrollment
        fields = ['course', 'term', 'year', 'user']
        # extra_kwargs = {
        #     'course': {'write_only': True},
        #     'term': {'write_only': True},
        #     'year': {'write_only': True}
        # }

    # def create(self, validated_data):
    #     if 'user' not in validated_data:
    #         validated_data['user'] = self.context['request'].user


class DayEntrySerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(
    #     required=False,
    #     read_only=True,
    #     default=serializers.CurrentUserDefault
    # )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = DayEntry
        fields = ['assignment', 'date', 'duration', 'user']

    # def create(self, validated_data):
    #     if 'user' not in validated_data:
    #         validated_data['user'] = self.context['request'].user


class StudentSerializer(serializers.ModelSerializer):
    # courses = serializers.StringRelatedField(
    #     many=True,
    #     read_only=True
    # )
    courses = EnrollmentSerializer(many=True, read_only=True)
    day_entries = DayEntrySerializer(many=True, read_only=True)

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
        fields = ['url', 'name', 'id', 'subject',
                  'course_number', 'assignments']


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255)
