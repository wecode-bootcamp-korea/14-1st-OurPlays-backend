import json

from django.views import View
from django.http import JsonResponse
from django.db import transaction

from share.decorators import check_auth_decorator
from .models import (
                    Reservation,
                    )

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

class GenerateView(View):
    @transaction.atomic
    @check_auth_decorator
    def post(self, request):
        try:            
            data    = json.loads(request.body)
            user_id = request.user

            Reservation(
                        shooting_members_count = data["shooting_members_count"],
                        begin_datetime         = data["begin_datetime"],
                        finish_datetime        = data["finish_datetime"],
                        place_id               = data["place_id"],
                        status_id              = 1,
                        guest_user_id          = user_id,
                    ).save()

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

