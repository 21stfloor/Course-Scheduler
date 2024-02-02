from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import User, PermissionsMixin
from django.urls import reverse
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from schedulerpages.managers import CustomUserManager
from django.utils.http import int_to_base36
from django.contrib.auth.hashers import make_password
import uuid

# Create your models here.
ID_LENGTH = 30
DEVICE_ID_LENGTH = 15

DAYS_OF_THE_WEEK = (
    ('Mon', 'Monday'),
    ('Tues', 'Tuesday'),
    ('Wed', 'Wednesday'),
    ('Thurs', 'Thursday'),
    ('Fri', 'Friday'),
    ('Sat', 'Saturday'),   
)
def id_gen() -> str:
    """Generates random string whose length is `ID_LENGTH`"""
    return int_to_base36(uuid.uuid4().int)[:ID_LENGTH]


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(max_length=ID_LENGTH,
                          primary_key=True, default=id_gen, editable=False)
    email = models.EmailField(_("email address"), unique=True, blank=False)
    firstname = models.CharField(max_length=50, blank=True, null=True)
    middlename = models.CharField(max_length=50, blank=True, null=True)
    lastname = models.CharField(max_length=50, blank=True, null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = "User"


    def __str__(self):
        if self.firstname is None and self.lastname is None:
            return self.email
        return f'{self.firstname} {self.lastname}'
    
    def save(self, *args, **kwargs):
        if not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2')):
            self.password = make_password(self.password)
        
        super().save(*args, **kwargs)
    
    


class Departments(models.Model):
    department_choices = (
        ('TED', 'TEACHER EDUCATION DEPARTMENT'),
        ('CSD', 'COMPUTER STUDIES DEPARTMENT '),
        ('ED', 'ENGINEERING DEPARTMENT '),
        ('ND', 'NURSING DEPARTMENT'),
        ('TechEntrepD', 'TECHNOLOGY & ENTREPRENEURSHIP DEPARTMENT'),

    )
    department_name = models.CharField(max_length=100, choices=department_choices, default='TED')

    def __str__(self):
        return self.department_name
    
    class Meta:
        verbose_name_plural = "Departments"
        verbose_name = "Department"
        ordering = ['department_name']


class Course(models.Model):
    course_code = models.CharField(max_length=10, unique=True)
    course_year_block = models.CharField(max_length=100)
    descriptive_title = models.CharField(max_length=1000)
    lecture_units = models.FloatField(validators=[MinValueValidator(0)], default=0)
    laboratory_units = models.FloatField(validators=[MinValueValidator(0)], default=0)
    course_department = models.ForeignKey(Departments, on_delete=models.CASCADE, blank=False, null=False)
    total_units = models.FloatField(validators=[MinValueValidator(0)], default=0)
    adviser = models.CharField(max_length=100)

    def __str__(self):
        return self.course_code + '<br>' + self.course_year_block + '<br>' + self.adviser
    

class Instructor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    instructor_id = models.CharField(max_length=100, unique=True)
    instructor_name = models.CharField(max_length=100)
    instructor_department = models.ForeignKey(Departments, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return self.instructor_name

class Rooms(models.Model):
    room_types = (
        ('Lecture', 'Lecture'),
        ('Laboratory', 'Laboratory'),
    )
    
    room_name = models.CharField(max_length=100)
    room_capacity = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    room_type = models.CharField(max_length=100, choices=room_types, default='Lecture')
    room_department = models.ForeignKey(Departments, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return self.room_name
    
    class Meta:
        verbose_name_plural = "Rooms"
        verbose_name = "Room"
        ordering = ['room_name']
        
class Schedule(models.Model):  
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=False, null=False)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, blank=False, null=False)
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE, blank=False, null=False)
    day = models.CharField(max_length=10, choices=DAYS_OF_THE_WEEK, default='Mon')
    time_start = models.TimeField()
    time_end = models.TimeField()
    
    def __str__(self) -> str:
        return f'{self.course} - {self.instructor} - {self.room}'
    
    class Meta:
        verbose_name_plural = "Schedules"
        verbose_name = "Schedule"
        ordering = ['course', 'instructor', 'room']
        unique_together = ['course', 'instructor', 'room']
    
    def save(self, *args, **kwargs):
        self.course = self.course
        self.instructor = self.instructor
        self.room = self.room
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        
#make a model for static time from 7am to 7pm with 30 minutes interval
class Time(models.Model):
    time_slots = (
        ('7:00 AM', '7:00 AM'),
        ('7:30 AM', '7:30 AM'),
        ('8:00 AM', '8:00 AM'),
        ('8:30 AM', '8:30 AM'),
        ('9:00 AM', '9:00 AM'),
        ('9:30 AM', '9:30 AM'),
        ('10:00 AM', '10:00 AM'),
        ('10:30 AM', '10:30 AM'),
        ('11:00 AM', '11:00 AM'),
        ('11:30 AM', '11:30 AM'),
        ('12:00 PM', '12:00 PM'),
        ('12:30 PM', '12:30 PM'),
        ('1:00 PM', '1:00 PM'),
        ('1:30 PM', '1:30 PM'),
        ('2:00 PM', '2:00 PM'),
        ('2:30 PM', '2:30 PM'),
        ('3:00 PM', '3:00 PM'),
        ('3:30 PM', '3:30 PM'),
        ('4:00 PM', '4:00 PM'),
        ('4:30 PM', '4:30 PM'),
        ('5:00 PM', '5:00 PM'),
        ('5:30 PM', '5:30 PM'),
        ('6:00 PM', '6:00 PM'),
        ('6:30 PM', '6:30 PM'),
        ('7:00 PM', '7:00 PM'),
    )
    
    time_slot = models.CharField(max_length=10, choices=time_slots, default='7:00 AM')
    
    def __str__(self) -> str:
        return self.time_slot
    
    class Meta:
        verbose_name_plural = "Time Slots"
        verbose_name = "Time Slot"
        ordering = ['time_slot']
        unique_together = ['time_slot']
        
class CombinedCourseSchedule(models.Model):
    # add the time field here
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=False, null=False)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, blank=False, null=False)
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE, blank=False, null=False)
    time_slot = models.ForeignKey(Time, on_delete=models.CASCADE, blank=False, null=False)
    
    def __str__(self) -> str:
        return f'{self.course} - {self.instructor} - {self.room} - {self.time_slot}'
    
    class Meta:
        verbose_name_plural = "Combined Course Schedules"
        verbose_name = "Combined Course Schedule"
        ordering = ['course', 'instructor', 'room', 'time_slot']
        unique_together = ['course', 'instructor', 'room', 'time_slot']
    
    