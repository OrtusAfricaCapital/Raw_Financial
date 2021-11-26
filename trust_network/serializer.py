from rest_framework import serializers
from .models import *

class TrustNetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrustNetwork
        fields = ('channel','Name','Description')