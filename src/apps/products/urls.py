from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductView.as_view(), name='list'),
    path('<int:pk>/', views.ProductUpdateView.as_view(), name='product-update'),

    path('categories/', views.CategoryView.as_view(), name='categories-list'),
    path('categories/<int:pk>/', views.CategoryUpdateView.as_view(), name='category-update'),
]
