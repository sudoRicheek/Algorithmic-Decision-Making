from django.db import models

from question.models import AttentionChoice, ComprehensionChoice

class Worker(models.Model):
    worker_id = models.CharField(max_length=200, unique=True)
    attention_responses = models.ManyToManyField(AttentionChoice,blank=True)
    attention_all_attempted = models.BooleanField(default=False)
    attention_passed = models.BooleanField(default=False)

    comprehension_responses = models.ManyToManyField(ComprehensionChoice,blank=True)
    comprehension_all_attempted = models.BooleanField(default=False)
    comprehension_passed = models.BooleanField(default=False)

    type_work = models.IntegerField(default=-1)
    
    def __str__(self) -> str:
        return self.worker_id

