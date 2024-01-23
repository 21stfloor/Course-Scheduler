from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import User, PermissionsMixin
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from schedulerpages.managers import CustomUserManager
from django.utils.http import int_to_base36
import uuid

# Create your models here.
ID_LENGTH = 30
DEVICE_ID_LENGTH = 15


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
        return self.course_code


class Instructor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    instructor_id = models.CharField(max_length=100, unique=True)
    instructor_name = models.CharField(max_length=100)
    instructor_department = models.ForeignKey(Departments, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return self.instructor_name
