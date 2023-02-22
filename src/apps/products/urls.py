from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductView.as_view(), name='list'),
    path('<int:pk>/', views.ProductUpdateView.as_view(), name='product-update'),
]
