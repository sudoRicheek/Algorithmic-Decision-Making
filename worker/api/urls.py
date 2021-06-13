from django.shortcuts import get_object_or_404
from django.urls import path

from worker.api.views import (
    add_worker,
    get_attention_results,
    get_comprehension_results,
    get_worker_type,
    submit_worker_beliefs,
)

app_name = 'worker'
urlpatterns = [
    path('addworker/', add_worker, name='worker-api-add'),
    path('get_attention_results/', get_attention_results,
         name='worker-api-attention-check-results'),
    path('get_comprehension_results/', get_comprehension_results,
         name='worker-api-get-comprehension-results'),
    path('get_worker_type/', get_worker_type,
         name='worker-api-get-worker-type'),
    path('submit_worker_beliefs/', submit_worker_beliefs,
         name='worker-api-submit-worker-beliefs'),
]
