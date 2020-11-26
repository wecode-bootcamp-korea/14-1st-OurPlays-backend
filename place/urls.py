from django.urls import path
from .views import (
                    CreatePlaceView,
                    UpdateDeletePlaceView,
                    GetPlaceView,
                    GetDetailPlaceView,
                    GetPlaceWithCategoryView,
                    AddRatingView,
                    GetRatingsView,
                    RemoveRatingView,
                    PlacesFromCategoryView,
                    SearchView,
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
        path('/<int:place_id>/ratings', GetRatingsView.as_view()),
        path('/rating/<int:rating_id>', RemoveRatingView.as_view()),        
        path('/places/<int:category_id>', PlacesFromCategoryView.as_view()),
        path('/search/<str:search_text>', SearchView.as_view()),
        ]                
