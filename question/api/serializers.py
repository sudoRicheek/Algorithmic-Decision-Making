from rest_framework import serializers

from question.models import AttentionCheckQuestion

class AttentionCheckQuestionSerializer(serializers.Serializer):
    class Meta:
        model = AttentionCheckQuestion
        fields = ['id','question_text','date_posted']
    