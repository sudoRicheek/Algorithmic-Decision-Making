from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.shortcuts import get_object_or_404

from question.models import AttentionCheckQuestion, ComprehensionQuestion
from worker.models import Worker

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
