from django.urls import path
from .views import *


urlpatterns = [
    path('create_borrower/', create_borrower_view, name='create_borrower'),
    path('show_borrower/', BorrowerView.as_view(), name='show_borrowers'),
]