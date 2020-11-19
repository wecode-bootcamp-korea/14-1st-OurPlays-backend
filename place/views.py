import json
import jwt

from django.db.models import Q
from django.core import serializers
from django.http import JsonResponse
from django.views import View

from .models import (
                    Place,
                    PlaceImage,
                    Tag,
                    Category,
                    )
from user.models import User

from share.decorators import checkAuthDecorator
from share.utils import getValueFromToken


class AddPlaceView(View):
    #@checkAuthDecorator
    def post(self, request):
        '''
        11. delegate_place_image_url(실제론 이미지 파일이 날라오므로 이미지를 저장해야 함)
        12. surcharge_rule (추가인원 옵션값(1,2,3))
            옵션1. 추가인원이 할당인원보다 작을시(10명 수용인데 11~19명) : 50% 추가.
            인원이 할당인원보다 2배 이상 3배 미만시                      : 100% 추가.
            인원이 할당인원보다 3배 이상시                               : 150% 추가
            옵션2. 인당 5500원/시간 추가
            옵션3. 인당 11000원/시간 추가
        '''

        try:
            data    = json.loads(request.body)
            token   = request.headers['token']
            user_id = token #getValueFromToken(token, 'user_id')

            category = Category.objects.get(name = data['category'])
            place = Place.objects.create(
                        address                  = data['address'],
                        price_per_hour           = data['price_per_hour'],
                        area                     = data['area'],
                        floor                    = data['floor'],
                        maximum_parking_lot      = data['maximum_parking_lot'],
                        allowed_members_count    = data['allowed_members_count'],
                        description              = data['description'],
                        using_rule               = data['using_rule'],
                        info_nearby              = data['info_nearby'],
                        minimum_rental_hour      = data['minimum_rental_hour'],
                        delegate_place_image_url = data['delegate_place_image_url'],
                        surcharge_rule           = data['surcharge_rule'],
                        category_id              = category.id,
                        user_id                  = user_id,
                    )
            
            for image in data['images']:
                PlaceImage( 
                        url = image['url'],
                        place_id = place.id
                        ).save()

            for tag in data['tags']:
                Tag(
                    name = tag['tag']
                    ).save()
            
        except Exception as ex:
            #return JsonResponse({"message":"INVALID_REQUEST"}, status = 400)
            return JsonResponse({"message":ex}, status = 400)

        return JsonResponse({"message":"SUCCESS"}, status = 201)
        
class UpdatePlaceView(View):
    #@checkAuthDecorator
    def post(self, request):
        try:
            data                           = json.loads(request.body)
            token                          = request.headers['token']
            category                       = Category.objects.get(name = data['category'])
            
            place                          = Place.objects.get(id = data['id'])
            

            place.address                  = data['address']
            place.price_per_hour           = data['price_per_hour']
            place.area                     = data['area']
            place.floor                    = data['floor']
            place.maximum_parking_lot      = data['maximum_parking_lot']
            place.allowed_members_count    = data['allowed_members_count']
            place.description              = data['description']
            place.using_rule               = data['using_rule']
            place.info_nearby              = data['info_nearby']
            place.minimum_rental_hour      = data['minimum_rental_hour']
            place.delegate_place_image_url = data['delegate_place_image_url']
            place.surcharge_rule           = data['surcharge_rule']
            place.category_id              = category.id
            place.save()

            PlaceImage.objects.filter(id=place.id).delete()
            
            for image in data['images']:
                PlaceImage( 
                        url = image['url'],
                        place_id = place.id
                        ).save()

            for tag in data['tags']:
                if not Tag.objects.filter(name = tag['tag']).exists():
                    Tag(
                        name = tag['tag']
                        ).save()

        except self.model.DoesNotExist:
            return JsonResponse({"message":"NOT_EXIST"}, status = 400)

        except Exception as ex:
           #return JsonResponse({"message":"INVALID_REQUEST"}, status = 400)
           return JsonResponse({"message":ex}, status = 400)

        return JsonResponse({"message":"SUCCESS"}, status = 201)          

class DeletePlaceView(View):
    #@checkAuthDecorator
    def post(self, request):
        try:
            data     = json.loads(request.body)
            token    = request.headers['token']
            place_id = data["id"]
            user_id  = token #getValueFromToken(token, 'user_id')

            if not Place.objects.filter(user_id = user_id).exists():
                return JsonResponse({"message":"NOT_EXIST"}, status = 400)

            Place.objects.filter(id = place_id).delete()

        except Exception:
            return JsonResponse({"message":"INVALID_REQUEST"}, status = 400)

        return JsonResponse({"message":"SUCCESS"}, status = 201) 

