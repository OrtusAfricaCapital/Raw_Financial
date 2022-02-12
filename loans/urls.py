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
    path('loan_scoring/<str:uid>/', loan_scoring, name="loan_scoring"),
    path('payments/<str:loan_uuid>/', payment_view, name="payments"),
    path('edit_loan/<str:loan_uid>/', edit_loan_view, name="edit_loan"),
    path('delete_loan/<str:loan_uid>/', delete_loan_view, name="delete_loan"),
    path('payment_status/<str:transaction_id>/<str:loan_uuid>/', payment_status_view, name="payment_status"),

    #api
    path('api/loan_request/',loan_request, name="loan_request"),
    path('api/loan_status/<str:lr_id>/', loan_status, name='loan_status'),
]

