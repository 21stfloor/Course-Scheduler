from django.contrib import admin
from django.apps import apps
from django.contrib.auth.models import Group
from django_tables2 import RequestConfig
from .models import Course, Instructor, CustomUser, Departments, Rooms, Schedule
from .tables import CourseTable, ScheduleTable

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


@admin.register(CustomUser)
class AdminCustomUser(admin.ModelAdmin):
    pass

@admin.register(Departments)
class AdminDepartments(admin.ModelAdmin):
    list_display = ('department_name',)

    def get_queryset(self, request):
        return Departments.objects.all().order_by('department_name')

@admin.register(Schedule)
class ScheduleModelAdmin(admin.ModelAdmin):
    # list_display = ('course', 'instructor', 'room')

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        table = ScheduleTable(data=Schedule.objects.all())
        RequestConfig(request).configure(table)
        extra_context['schedule_table'] = table
        instructor_schedule = Schedule.objects.all()
        
        extra_context['instructor_schedule'] = instructor_schedule
        return super(ScheduleModelAdmin, self).changelist_view(
            request, extra_context=extra_context,
        )
# Register your ModelAdmin

admin.site.register(Course, CourseModelAdmin)

app_config = apps.get_app_config('schedulerpages')
models = app_config.get_models()

for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass

# admin.site.unregister((Group))
