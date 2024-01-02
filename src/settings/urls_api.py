from django.urls import path, include


urlpatterns = [
    # path('clients/', include('apps.clients.urls')),
    path('clients_requests/', include('apps.clients_requests.urls_api')),
    # path('products/', include('apps.products.urls')),
    # path('', include('apps.users.urls')),
]
