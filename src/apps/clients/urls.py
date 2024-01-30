from django.urls import path

from . import views

app_name = 'clients'

urlpatterns = [
    path('', views.ClientsView.as_view(), name='list'),
    path('<int:pk>/', views.ClientUpdateView.as_view(), name='profile'),

    path('register/', views.RegisterView.as_view(), name='register'),
    path('register_confirm/<token>/', views.RegisterConfirmView.as_view(), name='register-confirm'),
    path('answer/', views.AnswerViewSet.as_view(), name='answer'),
]
