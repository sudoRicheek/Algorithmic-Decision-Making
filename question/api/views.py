import random
import time
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.shortcuts import get_object_or_404

from question.models import AttentionCheckQuestion, AttentionChoice, ComprehensionBeliefChoice, ComprehensionBeliefQuestion, ComprehensionChoice, ComprehensionQuestion, PostExperimentalChoice, PostExperimentalQuestion
from worker.models import Worker


@api_view(['POST', ])
def post_att_check_response(request):
    # time.sleep(2)
    # If worker not found -> make worker
    if 'worker_id' in request.data.keys() and not Worker.objects.filter(worker_id=request.data.get("worker_id")).exists():
        new_worker = Worker(worker_id=request.data.get("worker_id", ""))
        new_worker.save()

    # Get worker -> add responses
    worker = get_object_or_404(
        Worker, worker_id=request.data.get("worker_id", -1))
    if worker.attention_passed:
        return Response({"status": "alreadyPassed"}, status=status.HTTP_400_BAD_REQUEST)
    if worker.attention_all_attempted:
        return Response({"status": "alreadyFailed"}, status=status.HTTP_400_BAD_REQUEST)

    q_list = [q.get('q_id', -1) for q in request.data.get("answers", [])]
    q_list = set(q_list)
    if len(q_list) != AttentionCheckQuestion.objects.all().count():
        return Response({"status": "All questions must be answered before submitting"}, status=status.HTTP_400_BAD_REQUEST)

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

    response_data = {}
    response_data["worker_id"] = worker.worker_id
    response_data["status"] = "Answers Submitted Successfully"
    response_data["attention_all_attempted"] = worker.attention_all_attempted
    response_data["attention_passed"] = worker.attention_passed

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST', ])
def post_comprehension_response(request):
    worker = get_object_or_404(
        Worker, worker_id=request.data.get("worker_id", -1))
    if not worker.attention_all_attempted:
        return Response({"status": "attentionNoAttempt"}, status=status.HTTP_400_BAD_REQUEST)
    if not worker.attention_passed:
        return Response({"status": "attentionFailed"}, status=status.HTTP_403_FORBIDDEN)
    if worker.comprehension_all_attempted:
        return Response({"status": "alreadyAttempted"}, status=status.HTTP_403_FORBIDDEN)

    q_list = [q.get('q_id', -1) for q in request.data.get("answers", [])]
    q_list = set(q_list)
    if len(q_list) != ComprehensionQuestion.objects.all().count():
        return Response({"status": "All questions must be answered before submitting"}, status=status.HTTP_400_BAD_REQUEST)

    correctCount = 0
    for answerDict in request.data.get("answers", []):
        q_id = answerDict.get('q_id', -1)
        c_id = answerDict.get('c_id', -1)
        if q_id == -1 or c_id == -1:
            return Response({"status": "q_id and c_id must be present"}, status=status.HTTP_400_BAD_REQUEST)

        question = get_object_or_404(ComprehensionQuestion, pk=q_id)
        choice = get_object_or_404(ComprehensionChoice, pk=c_id)

        worker.comprehension_responses.add(choice)
        correct_choices = question.comprehensionchoice_set.filter(
            is_answer=True)
        if choice in correct_choices:
            correctCount += 1

    if worker.comprehension_failed_times < 2:
        # Set the passing criteria. Right now all the answers need to be correct to pass
        if correctCount == ComprehensionQuestion.objects.all().count():
            worker.comprehension_passed = True
            worker.comprehension_all_attempted = True
            if worker.type_work == -1:
                # worker.type_work = random.randint(0, 1)
                worker.type_work = 0
        else:
            worker.comprehension_failed_times += 1
        worker.save()

    if worker.comprehension_failed_times == 2:
        worker.comprehension_all_attempted = True
        worker.comprehension_passed = False
        worker.save()

    response_data = {}
    response_data["worker_id"] = worker.worker_id
    response_data["status"] = "Answers Submitted Successfully"
    response_data["comprehension_all_attempted"] = worker.comprehension_all_attempted
    response_data["comprehension_failed_times"] = worker.comprehension_failed_times
    response_data["comprehension_passed"] = worker.comprehension_passed
    response_data["type_work"] = worker.type_work

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST', ])
def post_comprehension_belief_response(request):
    worker = get_object_or_404(
        Worker, worker_id=request.data.get("worker_id", -1))
    if not worker.attention_all_attempted:
        return Response({"status": "attentionNoAttempt"}, status=status.HTTP_400_BAD_REQUEST)
    if not worker.attention_passed:
        return Response({"status": "attentionFailed"}, status=status.HTTP_403_FORBIDDEN)
    if not worker.comprehension_all_attempted:
        return Response({"status": "comprehensionNoAttempt"}, status=status.HTTP_403_FORBIDDEN)
    if not worker.comprehension_passed:
        return Response({"status": "comprehensionFailed"}, status=status.HTTP_403_FORBIDDEN)
    if worker.comprehension_belief_all_attempted:
        return Response({"status": "alreadyAttempted"}, status=status.HTTP_400_BAD_REQUEST)

    q_list = [q.get('q_id', -1) for q in request.data.get("answers", [])]
    q_list = set(q_list)
    if len(q_list) != ComprehensionBeliefQuestion.objects.all().count():
        return Response({"status": "All questions must be answered before submitting"}, status=status.HTTP_400_BAD_REQUEST)

    correctCount = 0
    for answerDict in request.data.get("answers", []):
        q_id = answerDict.get('q_id', -1)
        c_id = answerDict.get('c_id', -1)
        if q_id == -1 or c_id == -1:
            return Response({"status": "q_id and c_id must be present"}, status=status.HTTP_400_BAD_REQUEST)

        question = get_object_or_404(ComprehensionBeliefQuestion, pk=q_id)
        choice = get_object_or_404(ComprehensionBeliefChoice, pk=c_id)

        worker.comprehension_belief_responses.add(choice)
        correct_choices = question.comprehensionbeliefchoice_set.filter(
            is_answer=True)
        if choice in correct_choices:
            correctCount += 1

    if worker.comprehension_belief_failed_times < 2:
        # Set the passing criteria. Right now all the answers need to be correct to pass
        if correctCount == ComprehensionBeliefQuestion.objects.all().count():
            worker.comprehension_belief_passed = True
            worker.comprehension_belief_all_attempted = True
        else:
            worker.comprehension_belief_failed_times += 1
        worker.save()

    if worker.comprehension_belief_failed_times == 2:
        worker.comprehension_belief_all_attempted = True
        worker.comprehension_belief_passed = False
        worker.save()

    response_data = {}
    response_data["worker_id"] = worker.worker_id
    response_data["status"] = "Answers Submitted Successfully"
    response_data["comprehension_belief_all_attempted"] = worker.comprehension_belief_all_attempted
    response_data["comprehension_belief_failed_times"] = worker.comprehension_belief_failed_times
    response_data["comprehension_belief_passed"] = worker.comprehension_belief_passed
    response_data["type_work"] = worker.type_work

    return Response(response_data, status=status.HTTP_200_OK)


# @api_view(['POST', ])
# def post_postexperimental_response(request):
#     worker = get_object_or_404(
#         Worker, worker_id=request.data.get('worker_id', -1))
#     if not ((worker.decision_and_minoffer_submitted and worker.type_work == 0) or (worker.belief_elicitation_attempted and worker.type_work == 1)):
#         return Response({"status": "forbidden"}, status=status.HTTP_403_FORBIDDEN)

#     q_list = [q.get('q_id', -1) for q in request.data.get("responses", [])]
#     q_list = set(q_list)
#     if len(q_list) != PostExperimentalQuestion.objects.all().count():
#         return Response({"status": "All questions must be answered"}, status=status.HTTP_400_BAD_REQUEST)

#     for answerDict in request.data.get("responses", []):
#         q_id = answerDict.get('q_id', -1)
#         c_id = answerDict.get('c_id', -1)
#         if q_id == -1 or c_id == -1:
#             return Response({"status": "q_id and c_id must be present"}, status=status.HTTP_400_BAD_REQUEST)

#         question = get_object_or_404(PostExperimentalQuestion, pk=q_id)
#         choice = get_object_or_404(PostExperimentalChoice, pk=c_id)

#         worker.postexperimental_responses.add(choice)
#     worker.postexperimental_submitted = True
#     worker.save()

#     response_data = {}
#     response_data["worker_id"] = worker.worker_id
#     response_data["type_work"] = worker.type_work
#     response_data["status"] = "Answers Submitted Successfully"
#     response_data["postexperimental_submitted"] = worker.postexperimental_submitted

#     return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET', ])
def get_attention_questions(request):
    # time.sleep(2)
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


@api_view(['GET', ])
def get_comprehension_belief_questions(request):
    comprehension_belief_questions = ComprehensionBeliefQuestion.objects.all()
    data = {}
    data['questions'] = [{"id": question.id,
                          "question_text": question.question_text,
                          "date_posted": question.date_posted,
                          "choices": [{"id": choice.id,
                                       "choice_text": choice.choice_text,
                                       } for choice in question.comprehensionbeliefchoice_set.all()],
                          } for question in comprehension_belief_questions]
    return Response(data, status=status.HTTP_200_OK)


# @api_view(['POST', ])
# def get_postexperimental_questions(request):
#     worker = get_object_or_404(
#         Worker, worker_id=request.data.get("worker_id", -1))
#     if (worker.decision_and_minoffer_submitted and worker.type_work == 0) or (worker.belief_elicitation_attempted and worker.type_work == 1):
#         postexperimental_questions = PostExperimentalQuestion.objects.all()
#         data = {}
#         data['status'] = "pass"
#         data['type_work'] = worker.type_work
#         data['questions'] = [{"id": question.id,
#                               "question_text": question.question_text,
#                               "date_posted": question.date_posted,
#                               "choices": [{"id": choice.id,
#                                            "choice_text": choice.choice_text,
#                                            } for choice in question.postexperimentalchoice_set.all()],
#                               } for question in postexperimental_questions]
#         return Response(data, status=status.HTTP_200_OK)
#     return Response({"status": "fail"}, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST', ])
def get_dss_response(request):
    allocationSent = request.data.get("allocationSentToDSS", -1)
    print(allocationSent)
    if allocationSent not in [1, 2, 3, 4, 5, 6]:
        return Response({"status": "Bad Allocation"}, status=status.HTTP_400_BAD_REQUEST)

    # Dummy DSS
    response_data = {}
    response_data['allocationSentToDSS'] = allocationSent
    response_data['likelihoodAcceptanceValue'] = random.uniform(0, 1)
    response_data['likelihoodMaximumIncome'] = random.uniform(0, 1)
    return Response(response_data, status=status.HTTP_200_OK)
