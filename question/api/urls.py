from django.urls import path

from question.api.views import (
    get_attention_questions,
    get_comprehension_belief_questions,
    get_comprehension_questions,
#     get_postexperimental_questions,
    post_att_check_response,
    post_comprehension_belief_response,
    post_comprehension_response,
#     post_postexperimental_response,
    get_dss_response,
)

app_name = 'question'
urlpatterns = [
    path('post_attchk_response/', post_att_check_response,
         name='question-api-attention-check-response'),
    path('post_comp_response/', post_comprehension_response,
         name='question-api-comprehension-response'),
    path('post_comp_belief_response/', post_comprehension_belief_response,
         name='question-api-comprehension-belief-response'),
#     path('post_postexp_response/', post_postexperimental_response,
#          name='question-api-postexperimental-response'),
    path('get_attchk_questions/', get_attention_questions,
         name='question-api-get-all-attention-questions'),
    path('get_comp_questions/', get_comprehension_questions,
         name='question-api-get-all-comprehension-questions'),
    path('get_comp_belief_questions/', get_comprehension_belief_questions,
         name='question-api-get-all-comprehension-belief-questions'),
#     path('get_postexp_questions/', get_postexperimental_questions,
#          name='question-api-get-all-postexperimental-questions'),
    path('get_dss_response/', get_dss_response,
         name='question-api-get-dss-response'),
]
