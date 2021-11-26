from django.urls import path
from .views import *
from .api import *


urlpatterns = [
    path('create_trustnetwork/', create_tn_view, name='create_trustnetwork'),
    path('show_trustnetwork', TrustNetworkView.as_view(), name='show_trustnetwork'),

    #api urls
    path('api/trust_network/', trustnetwork_apiview, name='trust_network'),
]