import json
from datetime import datetime

from django.views import View
from django.http import JsonResponse
from django.db import transaction

from share.decorators import check_auth_decorator
from .models import (
                    Reservation,
                    )
from place.models import Place

@transaction.atomic
@check_auth_decorator
def update_reservation_status(request, status):
    '''
    reservation_status
    1:'예약신청',  2:'예약승인',  3:'결제완료', 4:'결제확인', 
    5:'예약불가',  6:'결제실패',  7:'예약취소'
    '''
    try:
        data                  = vjson.loads(request.body)
        user_id               = request.user       
        reservations          = Reservation.objects.filter(id = data["id"])

        if not reservations.exists():
            return JsonResponse({"message":"NOT_EXIST"}, status=400)

        reservation           = reservateions.get()
        reservation.status_id = status
        reservation.save()

        return JsonResponse({"message":"SUCCESS"}, status=201)

    except KeyError:
        return JsonResponse({"message":"KEY_ERROR"}, status=400)         

class CancelView(View):
    def post(self, request):
        return update_reservation_status(request, 7)
 
class ConfirmedGenerateView(View):
    def post(self, request):
        return update_reservation_status(request, 2)
        
class PayView(View):
    def post(self, request):
        return update_reservation_status(request, 3)
 
class ConfirmedPayView(View):
    def post(self, request):
        return update_reservation_status(request, 4)

class ReservationView(View):
    @transaction.atomic
    @check_auth_decorator
    def post(self, request):
        try:            
            data    = json.loads(request.body)
            user_id = request.user

            begin_datetime = f'{data["begin_date"]} {data["begin_time"]}'
            finish_datetime = f'{data["finish_date"]} {data["finish_time"]}'
            begin = datetime.strptime(begin_datetime, '%Y-%m-%d %H:%M')
            finish = datetime.strptime(finish_datetime, '%Y-%m-%d %H:%M')

            Reservation(
                        shooting_members_count = data["shooting_members_count"],
                        begin_datetime         = begin,                        
                        finish_datetime        = finish,
                        place_id               = data["place_id"],
                        status_id              = 1,
                        guest_user_id          = user_id,
                    ).save()

            return JsonResponse({"message":"SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

    @check_auth_decorator
    def get(self, request):
        try:            
            offset = int(request.GET.get('offset', 0))
            limit  = int(request.GET.get('limit', 20))

            result = [
                    {
                        'id'                     : reservation.id,
                        'host_name'              : reservation.place.user.name,
                        'img_url'                : reservation.place.delegate_place_image_url,
                        'place_id'               : reservation.place_id,
                        'shooting_members_count' : reservation.shooting_members_count,
                        'begin_datetime'         : reservation.begin_datetime,
                        'finish_datetime'        : reservation.finish_datetime,
                        'total_price'            : self.calculate_total_price(reservation),
                        'created_at'             : reservation.created_at,
                        'status'                 : reservation.status.status,
                        } for reservation in Reservation.objects.select_related('place', 'status', 'place__user').filter(guest_user_id = request.user)[offset:offset+limit]
            ]

            return JsonResponse({"message":"SUCCESS", "information":result}, status=200)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

    @check_auth_decorator
    def patch(self, request):
        try:
            data   = json.loads(request.body)

            reservations = Reservation.objects.filter(id = data["id"])

            if not reservations:
                return JsonResponse({"message":"NOT_EXIST"}, status=200)
            else:
                reservation = reservations.get()
                reservation.status_id = 7
                reservation.save()

            return JsonResponse({"message":"SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)


    def calculate_total_price(self, reservation):
        place            = Place.objects.get(id = reservation.place_id)
        overflow_members = place.allowed_members_count - reservation.shooting_members_count
        shooting_hours   = (reservation.finish_datetime - reservation.begin_datetime).seconds / 3600
        surcharge_pay    = 0

        if overflow_members > 0:
            if place.surcharge_rule == 2:
                surcharge_pay = overflow_members * shooting_hours * 5500
            elif place.surcharge_rule == 3:
                surcharge_pay = overflow_members * shooting_hours * 11000
            else:
                price_per_hour = place.allowed_members_count * place.price_per_hour
                surcharge_pay = price_per_hour * shooting_hours

                if overflow_members < place.allowed_members_count * 2:
                    surcharge_pay = surcharge_pay + (surcharge_pay / 2)
                elif overflow_members < place.allowed_members_count * 3:
                    surcharge_pay = surcharge_pay * 2
                elif overflow_members >= place.allowed_members_count * 3:
                    surcharge_pay = surcharge_pay + (surcharge_pay * 1.5)

        return surcharge_pay

