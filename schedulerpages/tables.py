import django_tables2 as tables
from .models import Course, Schedule


class CourseTable(tables.Table):

    class Meta:
        orderable = False
        model = Course
        template_name = "django_tables2/bootstrap.html"
        fields = ("course_code", "course_year_block", "descriptive_title", "lecture_units", "laboratory_units", "total_units", "adviser" )
        attrs = {'class': 'table table-bordered table-hover table-sm'}
        
class ScheduleTable(tables.Table):
    class Meta:
        orderable = False
        model = Schedule
        template_name = "django_tables2/bootstrap.html"
        fields = ("time_start", "instructor", "room", "day")
        attrs = {'class': 'table table-bordered table-hover table-sm table-primary table-striped'}