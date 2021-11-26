from rest_framework import serializers
from .models import *



class LoanRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanRequest
        fields = ('borrower_id','channel_id','loan_amount','loan_purpose','loan_duration','loan_request_date')






    