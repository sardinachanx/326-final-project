from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .constants import COURSE_SUBJECTS

# Create your models here.

# A model denoting an assignment. Assignments must be associated with
# a single course, and have a start and end date (for display
# purposes).
class Assignment(models.Model):
    ASSIGNMENT_TYPES = (
        ('PS', 'Problem Set'),
        ('QZ', 'Quiz'),
        ('EX', 'Exam'),
        ('PR', 'Presentation'),
        ('ES', 'Essay'),
        ('PJ', 'Project')
    )
    ASSIGNMENT_TO_STR = dict(ASSIGNMENT_TYPES)
    assigned_date = models.DateField()
    due_date = models.DateField()
    type = models.CharField(
        max_length=8, choices=ASSIGNMENT_TYPES, default='PS')
    number = models.PositiveSmallIntegerField(default=0)
    course = models.ForeignKey(
        'Course', on_delete=models.CASCADE, related_name='assignments')

    def __str__(self):
        return '%s, %s %s' % (self.course.__str__(), self.ASSIGNMENT_TO_STR[self.type], self.number)


# The "through" model used to identify the relationship between a
# course and a student. This should be the only endpoint in which
# a student and course can be connected (aka "enroll" a student).
# This database is write-only, unless admin needs to debug.
class Enrollment(models.Model):
    TERMS = [('F', 'Fall'), ('S', 'Spring')]
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    term = models.CharField(max_length=1, choices=TERMS)
    year = models.PositiveSmallIntegerField()


# The "profile" of a student. This is to denote any extra information,
# e.g. school, contact info, etc. associated with a user. Implemented
# for future extensibility; currently not tied to any other model.
class Student(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')

    def __str__(self):
        return self.user.__str__()


# Model denoting required information for a course. Maintains a list
# of students enrolled, but this should not be accessible.
class Course(models.Model):
    subject = models.CharField(max_length=8, choices=COURSE_SUBJECTS, default='')
    course_number = models.CharField(max_length=5)
    name = models.CharField(max_length=100)
    student = models.ManyToManyField(
        to='User', through=Enrollment, related_name='courses')
   #  professor = models.ForeignKey(Professor, on_delete=models.CASCADE)

    def __str__(self):
        return self.subject + ' ' + self.course_number + ': ' + self.name

    def get_course_id(self):
        return "%s %s" % (self.subject, self.course_number)


# Extended User class (as per Django conventions). "Removes" first and
# last name in place of a single name field. Email is the unique id,
# but username is also required (and should also be unique, as is
# originally the case in the Django base class). Should not contain any
# non-login-critical information; this should go to the Student model.
class User(AbstractUser):
    name = models.CharField(blank=True, max_length=255)
    first_name = models.CharField(blank=True, null=True, max_length=255)
    last_name = models.CharField(blank=True, null=True, max_length=255)
    email = models.EmailField(_('email'), unique=True)

    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'

    def __str__(self):
        return "%s (%s)" % (self.username, self.email)


# Model denoting required information to log hours for a particular
# assignment.
# TODO: add in validator/uniqueness check to make sure there isn't more
# than one entry for a given (assignment, date, user) tuple
class DayEntry(models.Model):
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='day_entries')
    assignment = models.ForeignKey(
        Assignment, on_delete=models.CASCADE, related_name='day_entries')
    date = models.DateField()
    duration = models.DurationField()


# Automates the creation of a profile entry in the Student databaes
# when a new user is created.
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Student.objects.create(user=instance)
    instance.profile.save()
