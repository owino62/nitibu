from rest_framework import serializers
from .models import Typhoid, Illness

class TyphoidSerializer(serializers.ModelSerializer):
    class Meta:
        model=Typhoid
        fields='__all__'


class IllnessSerializer(serializers.ModelSerializer):
    class Meta:
        model= Illness
        fields='__all__'