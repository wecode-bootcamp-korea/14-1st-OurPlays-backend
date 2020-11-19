from django.urls    import path
from .views         import PlaceView

urlpatterns =[
    path('placeview/',PlaceView.as_view()),
]  