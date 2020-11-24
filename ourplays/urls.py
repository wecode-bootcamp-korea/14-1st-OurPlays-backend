from django.urls import path, include

urlpatterns = [
        path('user', include('user.urls')),
        path('ProductList', include('place.urls')),
        path('reservation', include('reservation.urls')),
]
