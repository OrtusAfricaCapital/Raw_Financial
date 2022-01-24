from django.urls import path
from .views import *
from .api import *


urlpatterns = [
    path('create_borrower/<int:id>/', create_borrower_view, name='create_borrower'),
    path('show_borrower/', BorrowerView.as_view(), name='show_borrowers'),
    path('edit_borrower/<int:id>/', edit_borrower_view, name='edit_borrower'),
    path('create_borrower/', create_borrower, name='create_borrower'),
    path('delete_borrower/<int:id>/', delete_view, name='delete_borrower'),

    #api
    path('api/borrowers/', get_all_borrowers, name='all_borrowers'),
]