from django.contrib import admin
from django.apps import apps
from django_tables2 import RequestConfig
from .models import Course
from .tables import CourseTable
# Register your models here.
admin.site.site_header = "BU Polangui Course Scheduler"
admin.site.site_title = "BU Polangui Course Scheduler"
admin.site.index_title = ""

class CourseModelAdmin(admin.ModelAdmin):
    
     def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        table = CourseTable(data=Course.objects.all())
        RequestConfig(request).configure(table)
        extra_context['table'] = table
        return super(CourseModelAdmin, self).changelist_view(
            request, extra_context=extra_context,
        )

# Register your ModelAdmin

admin.site.register(Course, CourseModelAdmin)
app_config = apps.get_app_config('schedulerpages')
models = app_config.get_models()


