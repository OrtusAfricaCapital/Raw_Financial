from django import forms
from .models import *

class BorrowersForm(forms.ModelForm):
    class Meta:
        model = Borrower
        fields = ('tn','first_name', 'last_name','phone_number','email','address')

class BorrowerForm(forms.ModelForm):
    class Meta:
        model = Borrower
        fields = ('first_name', 'last_name','phone_number','email','address')