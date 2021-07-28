from django.contrib import admin
from django.db.models.query import QuerySet

from .models import AttentionCheckQuestion, AttentionChoice, ComprehensionBeliefChoice, ComprehensionBeliefQuestion, ComprehensionQuestion, ComprehensionChoice

admin.site.register([AttentionCheckQuestion, AttentionChoice,
                    ComprehensionQuestion, ComprehensionChoice,
                    # PostExperimentalQuestion, PostExperimentalChoice,
                    ComprehensionBeliefQuestion, ComprehensionBeliefChoice])
# Register your models here.
