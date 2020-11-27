from django.urls import path
from .views      import (
                        SignUpView,
                        SignInView,
                        MarkingPlaceView,
                        GetMarkedPlacesView,
                        SMSCheckView,
                        )

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/signin', SignInView.as_view()),
    path('/placemark', MarkingPlaceView.as_view()),
    path('/placemarks', GetMarkedPlacesView.as_view()),
    path('/authSMS', SMSCheckView.as_view()),
]
