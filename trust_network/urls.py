from django.urls import path
from .views import *


urlpatterns = [
    path('create_trustnetwork/', create_tn_view, name='create_trustnetwork'),
    path('show_trustnetwork', TrustNetworkView.as_view(), name='show_trustnetwork')
]