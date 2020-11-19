from django.urls import path
from .views import (
                    AddPlaceView,
                    UpdatePlaceView,
                    DeletePlaceView,
                    )

urlpatterns = [
        path('/add_place', AddPlaceView.as_view()),
        path('/update_place', UpdatePlaceView.as_view()),
        path('/delete_place', DeletePlaceView.as_view()),
        ]
