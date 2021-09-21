from django import forms
from .models import *

class BorrowerForm(forms.ModelForm):
    class Meta:
        model = Borrower
        fields = ('tn','first_name', 'last_name','phone_number','email','address')