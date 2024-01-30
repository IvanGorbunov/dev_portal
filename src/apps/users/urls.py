from django.urls import path, include

from . import views

app_name = 'users'

urlpatterns = [
    path('', views.LoginUser.as_view(), name='index'),

    path('users/', views.UserListView.as_view(), name='list'),
    path('users/<int:pk>/', views.UserUpdateView.as_view(), name='users-profile'),

    path('clients/', views.ClientListView.as_view(), name='clients-list'),
    path('clients/<int:pk>/', views.ClientUpdateView.as_view(), name='client-profile'),

    path('stuffs/', views.StuffListView.as_view(), name='stuffs-list'),
    path('stuffs/<int:pk>/', views.StuffUpdateView.as_view(), name='stuff-profile'),

    path('accounts/', include('django.contrib.auth.urls')),
]
