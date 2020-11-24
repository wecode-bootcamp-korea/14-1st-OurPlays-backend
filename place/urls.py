from django.urls import path
from .views import (
                    PlaceView,
                    )

urlpatterns = [
        path('', CreatePlaceView.as_view()),
        path('/<int:place_id>', UpdateDeletePlaceView.as_view()),
        ]
