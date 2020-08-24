# backend/server/apps/endpoints/serializers.py file
from rest_framework import serializers
from .models import DatosMovimiento

class DatosMovimientoSerializer(serializers.ModelSerializer):

    class Meta:
        model = DatosMovimiento
        fields = '__all__'