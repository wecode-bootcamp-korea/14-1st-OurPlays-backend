from django.urls import path
from .views import (
                    #GenerateView,
                    CancelView,
                    ConfirmedGenerateView,
                    PayView,
                    ConfirmedPayView,
                    #GetReservationsView,
                    ReservationView,
                )

urlpatterns = [
        #path("/generate", GenerateView.as_view()),
        path("/cancel", CancelView.as_view()),
        path("/confirm_generate", ConfirmedGenerateView.as_view()),
        path("/pay", PayView.as_view()),
        path("/confirm_pay", ConfirmedPayView.as_view()),
        #path("", GetReservationsView.as_view()),       
        path("", ReservationView.as_view()),       
        ]
