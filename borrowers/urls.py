from django.urls import path
from .views import *
from .api import *


urlpatterns = [
    path('create_borrower/<int:id>/', create_borrower_view, name='create_borrower'),
    path('show_borrower/', BorrowerView.as_view(), name='show_borrowers'),

    #api
    path('api/borrowers/', get_all_borrowers, name='all_borrowers'),
]