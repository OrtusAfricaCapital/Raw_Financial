from django.urls import path
from .views import *
from .api import *

urlpatterns = [
    path('create_loans/<int:id>', create_loan_view, name='create_loan'),
    path('show_loans/', LoanView.as_view(), name='show_loans'),
    path('loan_details/<int:id>', loan_details, name='loan_details'),
    path('loan_requests/', get_loan_requests, name='loan_requests'),
    path('loan_request_detail/<str:uid>/', loan_request_details, name='loan_request_detail'),
    path('issue_loan/<str:uid>/', give_loan, name="issue_loan"),

    #api
    path('api/loan_request/',loan_request, name="loan_request"),
    path('api/loan_status/<str:lr_id>/', loan_status, name='loan_status'),
]

