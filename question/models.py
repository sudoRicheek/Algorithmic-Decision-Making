from django.db import models


class AttentionCheckQuestion(models.Model):
    question_text = models.TextField(blank=True, null=True)
    date_posted = models.DateTimeField(
        auto_now_add=True, verbose_name="date posted", editable=False)

    def __str__(self) -> str:
        return self.question_text


class AttentionChoice(models.Model):
    question = models.ForeignKey(
        AttentionCheckQuestion, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_answer = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.choice_text


class ComprehensionQuestion(models.Model):
    question_text = models.TextField(blank=True, null=True)
    date_posted = models.DateTimeField(
        auto_now_add=True, verbose_name="date posted", editable=False)

    def __str__(self) -> str:
        return self.question_text


class ComprehensionChoice(models.Model):
    question = models.ForeignKey(
        ComprehensionQuestion, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_answer = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.choice_text


# class PostExperimentalQuestion(models.Model):
#     question_text = models.TextField(blank=True, null=True)
#     date_posted = models.DateTimeField(
#         auto_now_add=True, verbose_name="date posted", editable=False)

#     def __str__(self) -> str:
#         return self.question_text


# class PostExperimentalChoice(models.Model):
#     question = models.ForeignKey(
#         PostExperimentalQuestion, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)

#     def __str__(self) -> str:
#         return self.choice_text


class ComprehensionBeliefQuestion(models.Model):
    question_text = models.TextField(blank=True, null=True)
    date_posted = models.DateTimeField(
        auto_now_add=True, verbose_name="date posted", editable=False)

    def __str__(self) -> str:
        return self.question_text


class ComprehensionBeliefChoice(models.Model):
    question = models.ForeignKey(
        ComprehensionBeliefQuestion, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_answer = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.choice_text