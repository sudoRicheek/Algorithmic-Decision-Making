from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.shortcuts import get_object_or_404

from question.models import AttentionCheckQuestion, AttentionChoice, ComprehensionChoice, ComprehensionQuestion
from worker.models import Worker


@api_view(['POST', ])
def get_att_check_response(request):
    question = get_object_or_404(
        AttentionCheckQuestion, pk=request.data.get('q_id', -1))
    choice = get_object_or_404(
        AttentionChoice, pk=request.data.get('c_id', -1))

    # Check if worker exists later
    worker = get_object_or_404(Worker, worker_id=request.data.get('w_id', -1))

    worker.responses.add(choice)
    correct_choices = question.attentionchoice_set.filter(is_answer=True)
    if choice in correct_choices:
        return Response({"is_correct": "True"}, status=status.HTTP_200_OK)
    else:
        return Response({"is_correct": "False"}, status=status.HTTP_200_OK)


@api_view(['POST', ])
def get_comprehension_response(request):
    question = get_object_or_404(
        ComprehensionQuestion, pk=request.data.get('q_id', -1))
    choice = get_object_or_404(
        ComprehensionChoice, pk=request.data.get('c_id', -1))

    # Check if worker exists later
    worker = get_object_or_404(Worker, worker_id=request.data.get('w_id', -1))

    worker.responses.add(choice)
    # correct_choices = question.comprehensionchoice_set.filter(is_answer=True)
    return Response({"answered": "True"}, status=status.HTTP_200_OK)


@api_view(['GET', ])
def get_attention_questions(request):
    attentioncheck_questions = AttentionCheckQuestion.objects.all()
    data = {}
    data['questions'] = [{"id": question.id,
                          "question_text": question.question_text,
                          "date_posted": question.date_posted,
                          "choices": [{"id": choice.id,
                                       "choice_text": choice.choice_text,
                                    } for choice in question.attentionchoice_set.all()],
                          } for question in attentioncheck_questions]
    return Response(data, status=status.HTTP_200_OK)

