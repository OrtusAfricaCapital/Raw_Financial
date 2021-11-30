from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Loans)
admin.site.register(Payment)
admin.site.register(LoanRequest)
admin.site.register(LoanRequestStatus)
