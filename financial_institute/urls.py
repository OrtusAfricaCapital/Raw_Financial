from django.urls import path
from .views import *

urlpatterns = [
    path('create_fi/', create_fi_view, name='create_fi'),
    path('show_fi/', FIView.as_view(), name='show_fi'),
    path('investor_details/<int:id>/', investor_details_view, name='investor_details'),
]