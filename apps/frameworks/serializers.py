from rest_framework import serializers
from apps.base.serializers import BaseSerializer
from .models import Framework, Obligation, Clause, Control


class FrameworkSerializer(BaseSerializer, serializers.ModelSerializer):
    class Meta:
        model = Framework
        fields = '__all__'


class ObligationSerializer(BaseSerializer, serializers.ModelSerializer):
    class Meta:
        model = Obligation
        fields = '__all__'


class ClauseSerializer(BaseSerializer, serializers.ModelSerializer):
    class Meta:
        model = Clause
        fields = '__all__'


class ControlSerializer(BaseSerializer, serializers.ModelSerializer):
    class Meta:
        model = Control
        fields = '__all__'