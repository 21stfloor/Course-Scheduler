import django_tables2 as tables
from .models import Course


class CourseTable(tables.Table):

    class Meta:
        orderable = False
        model = Course
        template_name = "django_tables2/bootstrap.html"
        fields = ("course_code", "course_year_block", "descriptive_title", "lecture_units", "laboratory_units", "total_units", "adviser" )
        attrs = {'class': 'table table-hover shadow records-table table-bordered'}
        # row_attrs = {
        #     "onClick": lambda record: f"document.location.href='{reverse('system:order-detail', kwargs={'pk': record.pk})}';"
        # }
