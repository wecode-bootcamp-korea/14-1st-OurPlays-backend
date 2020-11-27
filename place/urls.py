from django.urls import path
from .views import (
                    #CreatePlaceView,
                    UpdateDeletePlaceView,
                    PlaceView,
                    GetDetailPlaceView,
                    #GetPlaceWithCategoryView,
                    #AddRatingView,
                    RatingsView,
                    RemoveRatingView,
                    #PlacesFromCategoryView,
                    #SearchView,
                    )

urlpatterns = [
        #path('', CreatePlaceView.as_view()),
        path('/<int:place_id>', UpdateDeletePlaceView.as_view()),
        path('', PlaceView.as_view()),
        path('/detail/<int:place_id>', GetDetailPlaceView.as_view()),
        #path('/ProductDetail/<str:category>', GetPlaceWithCategoryView.as_view()),
        #path('/rating', AddRatingView.as_view()),
        path('/<int:place_id>/ratings', RatingsView.as_view()),
        path('/rating/<int:rating_id>', RemoveRatingView.as_view()),        
        #path('/places/<int:category_id>', PlacesFromCategoryView.as_view()),
        #path('/search/<str:search_text>', SearchView.as_view()),
        ]                
