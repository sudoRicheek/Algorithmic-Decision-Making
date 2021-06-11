from rest_framework import status
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
def set_worker_type(request):
    worker = get_object_or_404(Worker, worker_id=request.data.get("w_id", -1))
    # Insert additional checks to ensure attention check and comprehension
    # sections have been passed.
    if worker.type_work == -1:
        worker.type_work = random.randint(0, 1)
        worker.save()
        return Response({"worker_id": worker.worker_id,
                        "type_work": worker.type_work}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Already worker type decided"}, status=status.status.HTTP_400_BAD_REQUEST)


@api_view(['POST', ])
def get_worker_type(request):
    worker = get_object_or_404(Worker, worker_id=request.data.get("w_id", -1))
    return Response({"worker_id": worker.worker_id,
                    "type_work": worker.type_work}, status=status.HTTP_200_OK)
