from django.contrib import admin
from django.contrib.auth.models import User, Group

from django.core.exceptions import PermissionDenied

from django.http import HttpResponse

import csv

from .models import Worker

admin.site.site_header = 'ADM HIT - Dashboard'


@admin.action(description='Download selected as csv')
def download_csv(modeladmin, request, queryset):
    if not request.user.is_staff:
        raise PermissionDenied

    model = queryset.model
    model_fields = model._meta.fields + model._meta.many_to_many
    field_names = [field.name for field in model_fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="export.csv"'

    writer = csv.writer(response, delimiter=",")
    writer.writerow(field_names)
    for row in queryset:
        values = []
        for field in field_names:
            value = getattr(row, field)
            if callable(value):
                try:
                    value = [str(x) for x in value.all()] or ''
                except:
                    value = 'Error retrieving value'
            if value is None:
                value = ''
            values.append(value)
        writer.writerow(values)
    return response


class WorkerAdmin(admin.ModelAdmin):
    list_display = ('worker_id',
                    'attention_passed',
                    'comprehension_passed',
                    'type_work',
                    'belief_elicitation_attempted',
                    'postexperimental_submitted')
    list_filter = ('attention_passed', 'comprehension_passed')
    ordering = ['worker_id']
    actions = [download_csv]


admin.site.register(Worker, WorkerAdmin)
admin.site.unregister([User, Group])
