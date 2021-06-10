from django.urls import path

from question.api.views import (
    get_attention_questions,
    get_comprehension_questions,
    post_att_check_response,
    post_comprehension_response,
)

app_name = 'question'
urlpatterns = [
    path('post_attchk_response/', post_att_check_response,
         name='question-api-attention-check-response'),
    path('post_comp_response/', post_comprehension_response,
         name='question-api-comprehension-response'),
    path('get_attchk_questions/', get_attention_questions,
         name='question-api-get-all-attention-questions'),
    path('get_comp_questions/', get_comprehension_questions,
         name='question-api-get-all-comprehension-questions')
]
