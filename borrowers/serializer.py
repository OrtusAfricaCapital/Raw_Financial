from rest_framework import serializers
from .models import *


class BorrowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrower
        fields = ('channel_borrower_uid','tn','first_name','last_name','phone_number','email','address')