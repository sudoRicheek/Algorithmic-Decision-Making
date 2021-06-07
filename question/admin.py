from django.contrib import admin
from django.db.models.query import QuerySet

from .models import AttentionCheckQuestion, AttentionChoice, ComprehensionQuestion, ComprehensionChoice

admin.site.register([AttentionCheckQuestion, AttentionChoice,
                    ComprehensionQuestion, ComprehensionChoice])
# Register your models here.
