from django.urls import path

from question.api.views import (
    get_att_check_response,
    get_comprehension_response,
)

app_name = 'question'
urlpatterns = [
    path('send_attchk_response/', get_att_check_response,
         name='question-api-attention-check-response'),
    path('get_comp_response/', get_comprehension_response,
         name='question-api-comprehension-response'),
]
