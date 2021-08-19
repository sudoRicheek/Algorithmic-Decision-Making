from django.contrib import admin

from .models import ComprehensionBeliefChoice, ComprehensionBeliefQuestion, ComprehensionQuestion, ComprehensionChoice

admin.site.register([ComprehensionQuestion, ComprehensionChoice,
                    ComprehensionBeliefQuestion, ComprehensionBeliefChoice])
# Register your models here.
