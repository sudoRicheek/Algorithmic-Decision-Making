from rest_framework import status
from rest_framework import response
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.shortcuts import get_object_or_404

from question.models import AttentionCheckQuestion, AttentionChoice, ComprehensionChoice, ComprehensionQuestion
from worker.models import Worker


@api_view(['POST', ])
def post_att_check_response(request):
    if len(request.data.get("answers", [])) != AttentionCheckQuestion.objects.all().count():
        return Response({"status": "All questions must be answered before submitting"}, status=status.HTTP_400_BAD_REQUEST)
    worker = get_object_or_404(
        Worker, worker_id=request.data.get("worker_id", -1))
    if worker.attention_all_attempted:
        return Response({"status": "Worker has already attempted Attention Test"}, status=status.HTTP_403_FORBIDDEN)

    correctCount = 0
    for answerDict in request.data.get("answers", []):
        q_id = answerDict.get('q_id', -1)
        c_id = answerDict.get('c_id', -1)
        if q_id == -1 or c_id == -1:
            return Response({"status": "q_id and c_id must be present"}, status=status.HTTP_400_BAD_REQUEST)

        question = get_object_or_404(AttentionCheckQuestion, pk=q_id)
        choice = get_object_or_404(AttentionChoice, pk=c_id)

        worker.attention_responses.add(choice)
        correct_choices = question.attentionchoice_set.filter(is_answer=True)
        if choice in correct_choices:
            correctCount += 1

    worker.attention_all_attempted = True
    # Set whatever the passign criteria
    if correctCount == AttentionCheckQuestion.objects.all().count():
        worker.attention_passed = True
    worker.save()

    return Response({"status": "Answers Submitted Successfully"}, status=status.HTTP_200_OK)


@api_view(['POST', ])
def post_comprehension_response(request):
    if len(request.data.get("answers", [])) != ComprehensionQuestion.objects.all().count():
        return Response({"status": "All questions must be answered before submitting"}, status=status.HTTP_400_BAD_REQUEST)
    worker = get_object_or_404(
        Worker, worker_id=request.data.get("worker_id", -1))
    if worker.comprehension_all_attempted:
        return Response({"status": "Worker has already attempted Comprehension Test"}, status=status.HTTP_403_FORBIDDEN)

    correctCount = 0
    for answerDict in request.data.get("answers", []):
        q_id = answerDict.get('q_id', -1)
        c_id = answerDict.get('c_id', -1)
        if q_id == -1 or c_id == -1:
            return Response({"status": "q_id and c_id must be present"}, status=status.HTTP_400_BAD_REQUEST)

        question = get_object_or_404(ComprehensionQuestion, pk=q_id)
        choice = get_object_or_404(ComprehensionChoice, pk=c_id)

        worker.comprehension_responses.add(choice)
        correct_choices = question.comprehensionchoice_set.filter(is_answer=True)
        if choice in correct_choices:
            correctCount += 1

    worker.comprehension_all_attempted = True
    # Set whatever the passign criteria
    if correctCount == ComprehensionQuestion.objects.all().count():
        worker.comprehension_passed = True
    worker.save()

    return Response({"status": "Answers Submitted Successfully"}, status=status.HTTP_200_OK)



@api_view(['GET', ])
def get_attention_questions(request):
    attentioncheck_questions = AttentionCheckQuestion.objects.all()
    data = {}
    data['questions'] = [{"id": question.id,
                          "question_text": question.question_text,
                          "choices": [{"id": choice.id,
                                       "choice_text": choice.choice_text,
                                       } for choice in question.attentionchoice_set.all()],
                          } for question in attentioncheck_questions]
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET', ])
def get_comprehension_questions(request):
    comprehension_questions = ComprehensionQuestion.objects.all()
    data = {}
    data['questions'] = [{"id": question.id,
                          "question_text": question.question_text,
                          "date_posted": question.date_posted,
                          "choices": [{"id": choice.id,
                                       "choice_text": choice.choice_text,
                                       } for choice in question.comprehensionchoice_set.all()],
                          } for question in comprehension_questions]
    return Response(data, status=status.HTTP_200_OK)
