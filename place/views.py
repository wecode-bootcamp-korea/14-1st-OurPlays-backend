import json
import jwt
import datetime
from decimal import Decimal

from django.core import serializers
from django.http import JsonResponse
from django.views import View
from django.db import transaction

from .models import (
                    Place,
                    PlaceImage,
                    Tag,
                    Category,
                    InvalidBookingDay,
                    )
from user.models import User

from share.decorators import check_auth_decorator
from share.utils import get_value_from_token


class AddPlaceView(View):
    @transaction.atomic
    #@check_auth_decorator
    def post(self, request):
        try:
            data       = json.loads(request.body)
            token      = request.headers['token']
            user_id    = token #get_value_from_token(token, 'user_id')            
            categories = Category.objects.filter(name = data['category'])
        
            if not categories:
                return JsonResponse({"message":"NOT_EXIST"}, status=400)
            
            category   = categories.get()
            place      = Place.objects.create(
                                    address                  = data['address'],
                                    price_per_hour           = Decimal(data['price_per_hour']),
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
            
            bulk_list = []

            for image in data['images']:
                bulk_list.append(PlaceImage( 
                                            url      = image['url'],
                                            place_id = place.id
                                            ))
            PlaceImage.objects.bulk_create(bulk_list)

            for tag in data['tags']:
                target_tag = None
                if not Tag.objects.filter(name = tag['tag']).exists():
                    target_tag = Tag.objects.create(name = tag['tag'])
                else:
                    target_tag = Tag.objects.get(name = tag['tag'])

                target_tag.places_tags.add(place)

            bulk_list.clear()

            for day in data['invalid_dates']:
                bulk_list.append(InvalidBookingDay(
                                            place_id = place.id,
                                            day      = datetime.datetime.strptime(
                                                                                day['date'],
                                                                                '%Y-%m-%d'
                                                                                )))
            InvalidBookingDay.objects.bulk_create(bulk_list)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status = 400)
            
        return JsonResponse({"message":"SUCCESS"}, status = 201)
        
class UpdatePlaceView(View):
    @transaction.atomic
    #@check_auth_decorator
    def post(self, request):
        try:
            data                           = json.loads(request.body)
            token                          = request.headers['token']
            categories                     = Category.objects.filter(name = data['category'])
            if not categories:
                return JsonResponse({"message":"NOT_EXIST"}, status=400)
             
            category                       = categories.get()
            places                         = Place.objects.filter(id = data['id'])
            if not places:
                return JsonResponse({"message":"NOT_EXIST"}, status=400)

            place                          = places.get()            
            place.address                  = data['address']
            place.price_per_hour           = Decimal(data['price_per_hour'])
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

            PlaceImage.objects.filter(place_id=place.id).delete()
            
            bulk_list = []

            for image in data['images']:
                bulk_list.append(PlaceImage( 
                                            url      = image['url'],
                                            place_id = place.id
                                            ))
            PlaceImage.objects.bulk_create(bulk_list)

            for tag in data['tags']:
                target_tag = None
                if not Tag.objects.filter(name = tag['tag']).exists():
                    target_tag = Tag.objects.create(name = tag['tag'])
                else:
                    target_tag = Tag.objects.get(name = tag['tag'])

                target_tag.places_tags.add(place)
            
            InvalidBookingDay.objects.filter(place_id = place.id).delete()

            bulk_list.clear()

            for day in data['invalid_dates']:
                bulk_list.append(InvalidBookingDay(
                                        place_id = place.id,
                                        day      = datetime.datetime.strptime(
                                                                        day['date'],
                                                                        '%Y-%m-%d'
                                                                        )))
            InvalidBookingDay.objects.bulk_create(bulk_list)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status = 400)

        return JsonResponse({"message":"SUCCESS"}, status = 201)          

class DeletePlaceView(View):
    @transaction.atomic
    #@check_auth_decorator
    def post(self, request):
        try:
            data     = json.loads(request.body)
            token    = request.headers['token']
            place_id = data["id"]
            user_id  = token #get_value_from_token(token, 'user_id')

            Place.objects.filter(id = place_id).delete()

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

        return JsonResponse({"message":"SUCCESS"}, status = 201) 

