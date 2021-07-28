from django.contrib.postgres.fields import ArrayField
from django.db import models

from question.models import AttentionChoice, ComprehensionBeliefChoice, ComprehensionChoice


class Worker(models.Model):
    worker_id = models.CharField(max_length=200, unique=True)
    attention_responses = models.ManyToManyField(AttentionChoice, blank=True)
    attention_all_attempted = models.BooleanField(default=False)
    attention_passed = models.BooleanField(default=False)

    svo_selected_indices = ArrayField(models.IntegerField(
        default=-1, blank=True), default=list)
    negative_reciprocity = ArrayField(models.IntegerField(
        default=-1, blank=True), default=list)
    sex = models.CharField(max_length=10, blank=True)
    age = models.IntegerField(default=1)
    employment_status = models.CharField(max_length=100, blank=True)
    highest_degree = models.CharField(max_length=100, blank=True)
    survey_submitted = models.BooleanField(default=False)

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

    dssProposerAllocation = models.IntegerField(default=-1)

    belief_elicitation = ArrayField(ArrayField(models.IntegerField(
        default=-1, blank=True), default=list), default=list)
    belief_elicitation_attempted = models.BooleanField(default=False)

    # 1 is Human
    # 2 is Human + DSS
    # 3 is Autonomous Agent
    # These fields are only exclusive to Responders! type_work = 0
    approach_decision = models.IntegerField(default=-1)  # from 1 to 3
    minimum_offer = models.IntegerField(default=-1)  # from 1 to 6
    decision_and_minoffer_submitted = models.BooleanField(default=False)

    # postexperimental_responses = models.ManyToManyField(
    #     PostExperimentalChoice, blank=True)
    # postexperimental_submitted = models.BooleanField(default=False)

    # Post Experimental Question Fields
    reason_approach_postexp = models.CharField(max_length=512)
    rethink_approach_postexp = models.IntegerField(default=-1)
    unfair_postexp = ArrayField(models.IntegerField(
        default=-1, blank=True), default=list)
    dss_postexp = ArrayField(models.IntegerField(
        default=-1, blank=True), default=list)
    autonomousagent_postexp = ArrayField(models.IntegerField(
        default=-1, blank=True), default=list)
    attention_postexp = models.BooleanField(default=False)
    personality_postexp = ArrayField(models.IntegerField(
        default=-1, blank=True), default=list)
    most_responders_bargain_with_postexp = ArrayField(models.IntegerField(
        default=-1, blank=True), default=list)
    postexperimental_submitted = models.BooleanField(default=False)

    # Unique-code for marking completion of the survey
    unique_code = models.CharField(
        max_length=300, editable=False, blank=True)
    unique_code_generated = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.worker_id
