from rest_framework import status
from rest_framework import response
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.shortcuts import get_object_or_404

from question.models import AttentionCheckQuestion, ComprehensionQuestion
from worker.models import Worker

import os
import random
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

    if worker.type_work == 0:
        predictions = [predictions[:6],predictions[6:12],predictions[12:]]
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
