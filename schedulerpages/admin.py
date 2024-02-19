from django.contrib import admin
from django.apps import apps
from django.contrib.auth.models import Group
from django_tables2 import RequestConfig
from .models import Course, Instructor, CustomUser, Departments, Rooms, Schedule, Time, CombinedCourseSchedule
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
        
        instructor_schedule = Schedule.objects.all()

        extra_context['instructor_schedule'] = instructor_schedule
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


@admin.register(Rooms)
class AdminRooms(admin.ModelAdmin):
    # list_display = ('room_name', 'room_type', 'room_department')

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        # table = ScheduleTable(data=Rooms.objects.all())
        # RequestConfig(request).configure(table)
        # extra_context['schedule_table'] = table
        rooms_schedule = Rooms.objects.all()
        instructor_schedule = []
        room_filter = request.POST.get('roomFilter', '0')
        if room_filter:
            instructor_schedule = Schedule.objects.filter(room__id=int(room_filter))
        if not room_filter or room_filter == '0':
            instructor_schedule = Schedule.objects.all()
        
        extra_context['rooms_schedule'] = rooms_schedule
        extra_context['room_filter'] = str(room_filter)
        extra_context['instructor_schedule'] = instructor_schedule
        return super(AdminRooms, self).changelist_view(
            request, extra_context=extra_context,
        )
        
    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     room_id = request.GET.get('room')
    #     if room_id:
    #         qs = qs.filter(id=room_id)
    #     return qs

@admin.register(CombinedCourseSchedule)
class AdminCombinedCourseSchedule(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        
        course_schedule = Course.objects.all()
        instructor_schedule = []
        course_filter = request.POST.get('courseFilter', '0')
        if course_filter:
            instructor_schedule = Schedule.objects.filter(course__id=int(course_filter))
        if not course_filter or course_filter == '0':
            instructor_schedule = Schedule.objects.all()
        
        extra_context['course_schedule'] = course_schedule
        extra_context['course_filter'] = str(course_filter)
        extra_context['instructor_schedule'] = instructor_schedule
        return super(AdminCombinedCourseSchedule, self).changelist_view(
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

admin.site.unregister((Time))
