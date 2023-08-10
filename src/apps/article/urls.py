from django.urls import path

from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.ArticleView.as_view(), name='list'),
    path('<int:pk>/', views.ArticleUpdateView.as_view(), name='article-update'),
]
