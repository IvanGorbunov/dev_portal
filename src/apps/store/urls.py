from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('pricelist/', views.PriceListView.as_view(), name='pricelist-list'),
    path('pricelist/<int:pk>/', views.PriceListUpdateView.as_view(), name='pricelist-update'),
    path('pricelist/<int:pk>/download/', views.PriceListDownloadView.as_view(), name='pricelist-download'),
]
