from django.db import models
from django.contrib.auth.models import User 
# Create your models here.


class Course(models.Model):
    course_code = models.CharField(max_length=10, unique=True)
    course_year_block = models.CharField(max_length=100)
    descriptive_title = models.CharField(max_length=1000)
    lecture_units = models.FloatField(default=0)
    laboratory_units = models.FloatField(default=0)
    total_units = models.FloatField(default=0)
    adviser = models.CharField(max_length=100)

    def __str__(self):
        return self.course_code

class Departments(models.Model):
    pass