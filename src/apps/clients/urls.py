from django.urls import path

from . import views

app_name = 'clients'

urlpatterns = [
    path('', views.ClientsView.as_view(), name='list'),
    path('<int:pk>/', views.ClientUpdateView.as_view(), name='profile'),

    path('register/', views.RegisterViewSet.as_view(), name='register'),
    path('answer/', views.AnswerViewSet.as_view(), name='answer'),
]
