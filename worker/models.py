from django.contrib.postgres.fields import ArrayField
from django.db import models

from question.models import ComprehensionBeliefChoice, ComprehensionChoice


class Worker(models.Model):
    worker_id = models.CharField(max_length=200, unique=True)

    comprehension_responses = models.ManyToManyField(
        ComprehensionChoice, blank=True)
    comprehension_all_attempted = models.BooleanField(default=False)
    comprehension_failed_times = models.IntegerField(default=0)
    comprehension_passed = models.BooleanField(default=False)

    # -1 => Not decided
    # 0 => responder
    # 1 => proposer
    type_work = models.IntegerField(default=-1)

    comprehension_belief_responses = models.ManyToManyField(
        ComprehensionBeliefChoice, blank=True)
    comprehension_belief_all_attempted = models.BooleanField(default=False)
    comprehension_belief_failed_times = models.IntegerField(default=0)
    comprehension_belief_passed = models.BooleanField(default=False)


    belief_elicitation = ArrayField(ArrayField(models.IntegerField(
        default=-1, blank=True), default=list), default=list)
    belief_elicitation_attempted = models.BooleanField(default=False)

    # 1 => Alone
    # 2 => With AI-System
    # Proposer specific fields
    proposer_type = models.IntegerField(default=-1)
    proposer_offer = models.IntegerField(default=-1)

    trust_automation = ArrayField(models.IntegerField(
        default=-1, blank=True), default=list)
    do_responders_consider_dss_while_deciding_proposers = models.BooleanField(default=False)
    
    # 1 => Human
    # 2 => Human + AI
    # 3 => Autonomous AI-System
    which_proposer_you_would_choose_to_be = models.IntegerField(default=-1)
    if_resp_which_proposer_would_you_approach = models.IntegerField(default=-1)
    proposer_most_responders_approach = models.IntegerField(default=-1)
    i_think_responders = ArrayField(models.IntegerField(
        default=-1, blank=True), default=list)


    sex = models.CharField(max_length=10, blank=True)
    age = models.IntegerField(default=1)
    employment_status = models.CharField(max_length=100, blank=True)
    highest_degree = models.CharField(max_length=100, blank=True)
    survey_submitted = models.BooleanField(default=False)

    # Unique-code for marking completion of the survey
    unique_code = models.CharField(
        max_length=300, editable=False, blank=True)
    unique_code_generated = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.worker_id
