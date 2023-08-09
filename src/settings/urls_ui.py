from django.urls import path, include


urlpatterns = [
    path('', include('apps.users.urls')),

    path('clients/', include('apps.clients.urls')),
    path('clients_requests/', include('apps.clients_requests.urls')),
    path('products/', include('apps.products.urls')),
    path('store/', include('apps.store.urls')),
]
