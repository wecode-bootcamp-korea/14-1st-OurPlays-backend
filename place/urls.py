from django.urls import path
from .views import (
                    CreatePlaceView,
                    UpdateDeletePlaceView,
                    GetPlaceView,
                    GetDetailPlaceView,
                    GetPlaceWithCategoryView,
                    AddRatingView,
                    GetRatingView,
                    )

urlpatterns = [
        path('', CreatePlaceView.as_view()),
        path('/<int:place_id>', UpdateDeletePlaceView.as_view()),
        #path('/get_places', GetPlaceView.as_view()),
        #path('/get_places/<int:place_id>', GetDetailPlaceView.as_view()),
        path('/ProductDetail', GetPlaceView.as_view()),
        path('/ProductDetail/<int:place_id>', GetDetailPlaceView.as_view()),
        path('/ProductDetail/<str:category>', GetPlaceWithCategoryView.as_view()),
        path('/rating', AddRatingView.as_view()),
        path('/<int:place_id>/ratings', GetRatingView.as_view()),
        ]                
