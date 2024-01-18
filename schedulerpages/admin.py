from django.contrib import admin
from django.apps import apps
from .models import Course

# Register your models here.
admin.site.site_header = "BU Polangui Course Scheduler"
admin.site.site_title = "BU Polangui Course Scheduler"
admin.site.index_title = ""


admin.site.register(Course)
app_config = apps.get_app_config('schedulerpages')
models = app_config.get_models()


