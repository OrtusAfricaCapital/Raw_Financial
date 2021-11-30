from rest_framework import serializers
from .models import *



class LoanRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanRequest
        fields = ('channel_borrower_uid','channel_id','loan_amount','loan_purpose','loan_duration')


class LoanStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanRequestStatus
        fields = ('loan_status','loan_status_description','created_at')






    