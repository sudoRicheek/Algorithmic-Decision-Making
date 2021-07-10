from django.contrib import admin
from django.db.models.query import QuerySet

from .models import AttentionCheckQuestion, AttentionChoice, ComprehensionQuestion, ComprehensionChoice, PostExperimentalChoice, PostExperimentalQuestion

admin.site.register([AttentionCheckQuestion, AttentionChoice,
                    ComprehensionQuestion, ComprehensionChoice,
                    PostExperimentalQuestion, PostExperimentalChoice])
# Register your models here.
