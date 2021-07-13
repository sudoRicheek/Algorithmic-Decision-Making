from django.contrib import admin
from django.contrib.auth.models import User, Group

from .models import Worker

admin.site.site_header = 'ADM HIT - Dashboard'

class WorkerAdmin(admin.ModelAdmin):
    list_display = ('worker_id', 
            'attention_passed', 
            'comprehension_passed', 
            'type_work', 
            'belief_elicitation_attempted', 
            'postexperimental_submitted')
    list_filter = ('attention_passed','comprehension_passed')

admin.site.register(Worker, WorkerAdmin)
admin.site.unregister([User, Group])
