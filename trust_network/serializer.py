from django.db.models import fields
from rest_framework import serializers
from .models import *

class TrustNetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrustNetwork
        fields = ('trustnetwork_uid','channel','Name','Description')

class TrustNetworkStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrustNetworkStatus
        fields = ('active_status',)