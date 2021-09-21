from django.urls import path
from .views import *


urlpatterns = [
    #path('create/', DepositCreateView.as_view(), name='create_deposit'),
    path('show_wallet/', show_wallet, name='show_wallet'),
    path('deposit/', deposit_view, name='deposit'),
    path('withdraw/', withdraw_view, name='withdraw'),
    
    #path('show_wallet/', Transaction.as_view(), name='show_transactions')
]