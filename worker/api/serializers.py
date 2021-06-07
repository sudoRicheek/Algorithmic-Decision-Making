from rest_framework import serializers

from worker.models import Worker

class WorkerSerializer(serializers.Serializer):
    class Meta:
        model = Worker
        fields = ['id','worker_id']
    