from django.urls import path
from rest_framework import routers

from .view.api_clients_requests import ClientsRequestsViewSet
from .view import api_clients_requests as views

app_name = 'clients_requests'

# clients_requests = routers.DefaultRouter()
# clients_requests.register(r'/', ClientsRequestsViewSet, 'transaction')

# urlpatterns = list(clients_requests.urls)

urlpatterns = [
    path('', views.ClientsRequestsViewSet.as_view({'get': 'list'}), name='list'),
#     path('add/', views.ClientsRequestCreateView.as_view(), name='clients-request-add'),
#     path('<int:pk>/', views.ClientsRequestUpdateView.as_view(), name='clients-request-update'),
#     path('<int:pk>/delete/', views.ClientsRequestDeleteView.as_view(), name='clients-request-delete'),
#     path('<int:pk>/add_attachment/', views.ClientsRequestAddAttachmentView.as_view({'post': 'add_attachment'}), name='clients-request-add-attachment'),
#
#     path('export_to_excel/', views.ExportClientsRequestsView.as_view({'get': 'export_to_excel'}), name='clients-request-export-xlsx'),
#
]
