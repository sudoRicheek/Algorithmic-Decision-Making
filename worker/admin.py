from django.contrib import admin
from django.contrib.auth.models import User, Group

from .models import Worker

admin.site.site_header = 'ADM HIT - Dashboard'

class WorkerAdmin(admin.ModelAdmin):
    list_display = ()
    list_filter = ()
    

admin.site.register(Worker)
admin.site.unregister([User, Group])
