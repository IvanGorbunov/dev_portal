from django.urls import path
from .view import api_clients_requests as views

app_name = 'clients_requests'

urlpatterns = [
    path('', views.ClientsRequestsViewSet.as_view({'get': 'list'}), name='list'),
]
