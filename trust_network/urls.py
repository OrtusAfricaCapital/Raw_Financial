from django.urls import path
from .views import *
from .api import *


urlpatterns = [
    path('create_trustnetwork/', create_tn_view, name='create_trustnetwork'),
    path('show_trustnetwork', TrustNetworkView.as_view(), name='show_trustnetwork'),
    path('edit_trustnetwork/<int:id>/', edit_tn_view, name="edit_trustnetwork"),
    path('trust_network_details/<int:id>/', tn_details_view, name="trust_network_details"),
    path('delete_trust_network/<int:id>/', delete_trust_network, name="delete_trust_network"),

    #api urls
    path('api/trust_network/', trustnetwork_apiview, name='trust_network'),
    path('api/trustnetwork_status/<str:tn_id>/', trust_status, name='trustnetwork_status'),
]