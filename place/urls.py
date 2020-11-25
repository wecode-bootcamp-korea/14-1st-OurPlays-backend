from django.urls    import path
from .views         import ReviewsView,PlaceDetailView,SearchView,ReviewView,PlacesView

urlpatterns =[
    #path('test',Test.as_view()),
    path('reviews',ReviewsView.as_view()),
    path('reviews/<int:place_id>',ReviewsView.as_view()),
    path('review/<int:rating_id>',ReviewView.as_view()),
    path('',SearchView.as_view()),
    path('category/<int:category_id>',PlaceDetailView.as_view()),
    path('<int:category_id>',PlacesView.as_view()),


]  
