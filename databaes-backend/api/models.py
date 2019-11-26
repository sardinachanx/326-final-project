from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    ASSIGNMENT_TO_STR = dict(ASSIGNMENT_TYPES)
    assigned_date = models.DateField()
    due_date = models.DateField()
    type = models.CharField(
        max_length=2, choices=ASSIGNMENT_TYPES, default='PS')
    number = models.PositiveSmallIntegerField(default=0)
    course = models.ForeignKey(
        'Course', on_delete=models.CASCADE, related_name='assignments')
    
    def __str__(self):
        return '%s, %s %s' % (self.course.__str__(), self.ASSIGNMENT_TO_STR[self.type], self.number)


class Enrollment(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    term = models.CharField(max_length=1, choices=TERMS)
    year = models.IntegerField()


class Student(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    def __str__(self):
        return self.user.__str__()


class Course(models.Model):
    subject = models.CharField(max_length=7)
    course_number = models.CharField(max_length=5)
    name = models.CharField(max_length=100)
    student = models.ManyToManyField(
        to=Student, through=Enrollment, related_name='courses')
   #  professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    def __str__(self):
        return self.subject + ' ' + self.course_number + ': ' + self.name

    def get_course_id(self):
        return "%s %s" % (self.subject, self.course_number)


class User(AbstractUser):
    name = models.CharField(blank=True, max_length=255)
    first_name = models.CharField(blank=True, null=True, max_length=255)
    last_name = models.CharField(blank=True, null=True, max_length=255)
    email = models.EmailField(_('email'), unique=True)

    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'
    def __str__(self):
        return "%s (%s)" % (self.username, self.email)


class DayEntry(models.Model):
    student = models.ForeignKey(
        'Student', on_delete=models.CASCADE, related_name='day_entries')
    assignment = models.ForeignKey(
        Assignment, on_delete=models.CASCADE, related_name='day_entries')
    date = models.DateField()
    duration = models.DurationField()


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Student.objects.create(user=instance)
    instance.profile.save()
