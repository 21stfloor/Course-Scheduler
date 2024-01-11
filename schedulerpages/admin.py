from django.contrib import admin
from django.apps import apps

# Register your models here.
admin.site.site_header = "BU Polangui Course Scheduler"
admin.site.site_title = "BU Polangui Course Scheduler"
admin.site.index_title = ""

app_config = apps.get_app_config('schedulerpages')
models = app_config.get_models()


