from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

# Create your models here.

TERMS = [('F', 'Fall'), ('S', 'Spring')]

class Assignment(models.Model):
    ASSIGNMENT_TYPES = (
        ('PS', 'Problem Set'),
        ('QZ', 'Quiz'),
        ('EX', 'Exam'),
        ('PR', 'Presentation'),
        ('ES', 'Essay'),
        ('PJ', 'Project')
    )
    assigned_date = models.DateField()
    due_date = models.DateField()
    type = models.CharField(max_length=2, choices=ASSIGNMENT_TYPES, default='PS')
    number = models.PositiveSmallIntegerField(default=0)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)

class Enrollment(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    term = models.CharField(max_length=1, choices=TERMS)
    year = models.IntegerField()

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')

class Course(models.Model):
    subject = models.CharField(max_length=7)
    course_number = models.CharField(max_length=5)
    name = models.CharField(max_length=100)
    student = models.ManyToManyField(to=Student, through=Enrollment, related_name='courses')
   #  professor = models.ForeignKey(Professor, on_delete=models.CASCADE)

class User(AbstractUser):
    name = models.CharField(blank=True, max_length=255)
    first_name = models.CharField(blank=True, null=True)
    last_name = models.CharField(blank=True, null=True)
    email = models.EmailField(_('email_address'), unique=True)

    REQUIRED_FIELDS = ['username', 'email_address']
    USERNAME_FIELD = 'email'

class DayEntry(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    date = models.DateField()
    duration = models.DurationField()

