from django.urls import path
from .views import *

urlpatterns = [
    path('create_channel/', channel_view, name='create_channel'),
    path('show_channel/', ChannelView.as_view(), name='show_channel'),
    path('channel_details/<int:id>/', channel_details, name='channel_details'),
    path('edit_channel/<int:id>/', edit_channel_view, name='edit_channel'),
    path('delete_channel/<int:id>/', delete_channel, name='delete_channel'),
    path('channel_borrowers/<int:id>/', show_borrowers_in_network, name="channel_borrowers"),
    path('loan_borrowed/<int:id>', loan_borrower, name='loan_borrowed'),
    path('payment/<int:id>/', make_payment, name='payment'),
    
]