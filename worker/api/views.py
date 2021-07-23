from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.shortcuts import get_object_or_404, resolve_url

from question.models import AttentionCheckQuestion, ComprehensionQuestion
from worker.models import Worker

import secrets

from pytz import timezone


@api_view(['POST', ])
def add_worker(request):
    if request.method == 'POST':
        if request.data.get('worker_id', "") == "":
            return Response({"worker_id": "Can't be empty"}, status=status.HTTP_400_BAD_REQUEST)

        num_count = Worker.objects.filter(
            worker_id=request.data.get('worker_id', "")).count()

        # This will be changed later!!!!
        if num_count != 0:
            return Response({"worker_id": "Worker ID already present!"}, status=status.HTTP_200_OK)

        new_worker = Worker(worker_id=request.data.get('worker_id', ""))
        new_worker.save()
        return Response({"worker_id": request.data.get('worker_id', "")}, status=status.HTTP_201_CREATED)


@api_view(['POST', ])
def get_attention_results(request):
    # Handle if worker not present later
    worker = get_object_or_404(
        Worker, worker_id=request.data.get("worker_id", -1))
    return Response({"attempted": worker.attention_all_attempted, "passed": worker.attention_passed}, status=status.HTTP_200_OK)


@api_view(['POST', ])
def get_comprehension_results(request):
    # Handle if worker not present later
    worker = get_object_or_404(
        Worker, worker_id=request.data.get("worker_id", -1))
    return Response({"attempted": worker.comprehension_all_attempted, "passed": worker.comprehension_passed}, status=status.HTTP_200_OK)


@api_view(['POST', ])
def get_worker_type(request):
    worker = get_object_or_404(
        Worker, worker_id=request.data.get("worker_id", -1))
    response_data = {}

    response_data["comprehension_all_attempted"] = worker.comprehension_all_attempted
    response_data["comprehension_passed"] = worker.comprehension_passed
    response_data["type_work"] = worker.type_work
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST', ])
def submit_worker_beliefs(request):
    worker = get_object_or_404(
        Worker, worker_id=request.data.get("worker_id", -1))
    predictions = [e for e in request.data.get("predictions", [])]
    if worker.type_work == -1:
        return Response({"status": "forbidden"}, status=status.HTTP_403_FORBIDDEN)
    elif worker.type_work == 0:
        if len(predictions) != 18:
            return Response({"status": "18 predictions required"}, status=status.HTTP_400_BAD_REQUEST)
    elif worker.type_work == 1:
        if len(predictions) != 6:
            return Response({"status": "6 predictions expected"}, status=status.HTTP_400_BAD_REQUEST)
    if worker.belief_elicitation_attempted:
        return Response({"status": "alreadyAttempted"}, status=status.HTTP_403_FORBIDDEN)

    # Ensure row number is between 1 and 21
    if worker.type_work == 0:
        predictions = [predictions[:6], predictions[6:12], predictions[12:]]
    elif worker.type_work == 1:
        predictions = [predictions]

    worker.belief_elicitation = predictions
    worker.belief_elicitation_attempted = True
    worker.save()

    response_data = {}
    response_data['status'] = "beliefelicitation submitted"
    response_data['worker_id'] = worker.worker_id
    response_data['type_work'] = worker.type_work

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST', ])
def submit_approach_decision_minoffer(request):
    worker = get_object_or_404(
        Worker, worker_id=request.data.get("worker_id", -1))
    if worker.decision_and_minoffer_submitted:
        return Response({"status": "alreadySubmitted"}, status=status.HTTP_400_BAD_REQUEST)
    if not worker.belief_elicitation_attempted or worker.type_work != 0:
        return Response({"status": "forbidden"}, status=status.HTTP_403_FORBIDDEN)

    approach_decision = request.data.get("approach_decision", -1)
    if approach_decision not in [1, 2, 3]:
        return Response({"status": "badchoice"}, status=status.HTTP_400_BAD_REQUEST)

    minimum_offer = request.data.get("minimum_offer", -1)
    if minimum_offer not in [1, 2, 3, 4, 5, 6]:
        return Response({"status": "badchoice"}, status=status.HTTP_400_BAD_REQUEST)

    worker.approach_decision = approach_decision
    worker.minimum_offer = minimum_offer
    worker.decision_and_minoffer_submitted = True
    worker.save()

    response_data = {}
    response_data['status'] = "approach_decision submitted"
    response_data['worker_id'] = worker.worker_id
    response_data['approach_decision'] = worker.approach_decision
    response_data['minimum_offer'] = worker.minimum_offer
    response_data['approach_decision_minoffer_submitted'] = worker.decision_and_minoffer_submitted
    response_data['type_work'] = worker.type_work

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST', ])
def submit_dss_proposer_response(request):
    worker = get_object_or_404(
        Worker, worker_id=request.data.get("worker_id", -1))
    if worker.type_work != 1:
        return Response({"status": "notAllowedHere"}, status=status.HTTP_403_FORBIDDEN)

    if worker.dssProposerAllocation != -1:
        return Response({"status": "Already Submitted"}, status=status.HTTP_403_FORBIDDEN)

    allocationSubmitted = request.data.get('allocationSubmitted', -1)
    if allocationSubmitted not in [1, 2, 3, 4, 5, 6]:
        return Response({"status": "Bad Allocation"}, status=status.HTTP_400_BAD_REQUEST)

    worker.dssProposerAllocation = allocationSubmitted
    worker.save()

    response_data = {}
    response_data["status"] = "Allocation Submitted"
    response_data["worker_id"] = worker.worker_id
    response_data["allocationSubmitted"] = allocationSubmitted
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST', ])
def get_uniquecode(request):
    worker = get_object_or_404(
        Worker, worker_id=request.data.get("worker_id", -1))
    if worker.unique_code_generated:
        return Response({"status": "Unique Code", "unique_code": worker.unique_code}, status=status.HTTP_200_OK)

    if worker.attention_passed and worker.survey_submitted and worker.comprehension_passed and worker.comprehension_belief_passed and worker.belief_elicitation_attempted and worker.postexperimental_submitted:
        worker.unique_code = secrets.token_urlsafe(32)
        worker.unique_code_generated = True
        worker.save()
    else:
        return Response({"status": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

    response_data = {}
    response_data["status"] = "Unique Code"
    response_data["worker_id"] = worker.worker_id
    response_data["unique_code"] = worker.unique_code

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST', ])
def post_postexperimental_responder(request):
    worker = get_object_or_404(
        Worker, worker_id=request.data.get("worker_id", -1))
    if worker.postexperimental_submitted:
        return Response({"status": "alreadySubmitted"}, status=status.HTTP_400_BAD_REQUEST)

    reasonApproach = request.data.get("reasonApproach", "")
    rethinkApproach = request.data.get("rethinkApproach", -1)

    unfair = [e for e in request.data.get("unfair", [])]
    dss = [e for e in request.data.get("dss", [])]
    autonomousagent = [e for e in request.data.get("autonomousagent", [])]

    attentioncheck = request.data.get("attentioncheck", -1)
    personality = [request.data.get("personality", -1)]
    mostRespondersBargainWith = [
        request.data.get("mostRespondersBargainWith", -1)]

    worker.reason_approach_postexp = reasonApproach
    worker.rethink_approach_postexp = rethinkApproach
    worker.unfair_postexp = unfair
    worker.dss_postexp = dss
    worker.autonomousagent_postexp = autonomousagent
    worker.attention_postexp = (attentioncheck == 2)  # Hardcoded, lack of time
    worker.personality_postexp = personality
    worker.most_responders_bargain_with_postexp = mostRespondersBargainWith
    worker.postexperimental_submitted = True
    worker.save()

    return Response({"status": "Post Experimental Submitted Sucessfully"}, status=status.HTTP_200_OK)


@api_view(['POST', ])
def post_survey_responses(request):
    worker = get_object_or_404(
        Worker, worker_id=request.data.get("worker_id", -1))

    if worker.survey_submitted:
        return Response({"status": "alreadySubmitted"}, status=status.HTTP_400_BAD_REQUEST)

    nr = [e for e in request.data.get("nr", [])]
    sex = request.data.get("sex", '')
    age = request.data.get("age", 1)
    employmentStatus = request.data.get("employmentStatus", '')
    highestDegree = request.data.get("highestDegree", '')

    worker.negative_reciprocity = nr
    worker.sex = sex
    worker.age = age
    worker.employment_status = employmentStatus
    worker.highest_degree = highestDegree
    worker.survey_submitted = True
    worker.save()

    return Response({"status": "Survey Submitted Sucessfully"}, status=status.HTTP_200_OK)
