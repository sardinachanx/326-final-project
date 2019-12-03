from datetime import timedelta
from random import randint, sample

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from .models import Assignment, Course, DayEntry, Enrollment, User

# TODO: Unit tests! This framework works for functionality only...


# Setup for tests

# Set up database with specificed number of entries. 
# Number of assignments, day entries, and enrollment is randomly 
# generated. 
# 
# Parameters:
# - num_admins: Number of admins 
# - num_users: Number of non-admin users
# - num_courses: Number of unique courses
class BaseTestCase(APITestCase):
    def __init__(self, *args, **kwargs):
        self._dev_test_client = APIClient()
        self._num_admins = kwargs.pop('num_admins')
        self._num_users = kwargs.pop('num_users')
        self._num_courses = kwargs.pop('num_courses')
        super().__init__(*args, **kwargs)

    @staticmethod
    def create_user(email, username, name, password, is_admin):
        user = User.objects.create_user(username=username, email=email, 
            password=password, is_admin=is_admin, name=name)
        return user.pk

    @staticmethod 
    def create_course(subject, course_number, name): 
        course = Course.objects.create(subject=subject, name=name, course_number=course_number)
        return course.pk

    @staticmethod
    def enroll_student(student, course, term, year):
        Enrollment.objects.create(user=student, course=course, term=term, year=year)

    @staticmethod 
    def add_assignment(course, assignment_id):
        # TODO: implement method 
        pass  


    # Generates database setup with specified number of entries.
    # Assumes only one term. #TODO: adopt framework for more. 
    def setup(self):
        total_user_count = self._num_admins + self._num_users

        # Set up admins, users, courses according to count
        for i in range(self._num_admins):
            self.create_user(email='admin' + i + '@gmail.com', username='admin' + i,
                password='thisisadmin' + i + 'spassword', is_admin=True, name='Admin ' + i)
        
        for i in range(self._num_users):
            self.create_user(email='student' + i + '@gmail.com', username='student' + i,
                password='thisisstudent' + i + 'spassword', is_admin=False, name='Student ' + i)

        for i in range(self._num_courses):
            course = self.create_course(subject='TEST', course_number=randint(100, 999), name='Test Course ' + i)
            
            # Generate assignments 
            assignment_count = randint(0, 20)
            for assignment_id in assignment_count: 
                # Assume all assignments are problem sets 
                self.add_assignment(i, assignment_id)
            
            # Generate enrollment and day entries 
            students_in_course = sample(range(1, total_user_count), randint(0, total_user_count))
            for student in students_in_course:
                self.enroll_student(student, course, 'F', 2019)
                # TODO: finish method
                # TODO: generate day entries for students and add them! 

# Unit/Functional tests


# Test permission access of different API endpoints.
class PermissionsTest(BaseTestCaes):
    pass

# Test save/load of information. 
class SaveLoadTest(BaseTestCase):
    pass 


# Smoke Tests
