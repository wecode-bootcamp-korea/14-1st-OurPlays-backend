import json
import jwt
from decimal import Decimal

from django.db.models import (
                                Q,
                                Avg
                            )
from django.core import serializers
from django.http import JsonResponse
from django.views import View
from django.db  import transaction
from django.core.files.storage import FileSystemStorage

from PIL import Image
from io import BytesIO

from .models import (
                    Place,
                    PlaceImage,
                    Tag,
                    Category,
                    InvalidBookingDay,
                    Rating,
                    Region,
                    )
from user.models import User
from share.decorators import check_auth_decorator
from share.kakaomap import getLatLng


class CreatePlaceView(View):
    @transaction.atomic
    @check_auth_decorator
    def post(self, request):
        try:
            data       = json.loads(reqeust.body)
            categories = Category.objects.filter(name = data['category'])

            if not categories:
                return JsonResponse({"message":"NOT_EXIST"}, status=400)

            address    = data['address']
            category   = categories.get()
            place      = Place.objects.create(
                                    address                  = address,
                                    price_per_hour           = Decimal(data['price_per_hour']),
                                    region_id                = Region.objects.get(name=data['region']).id,
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
                                    latitude                 = getLatLng(address)[0],
                                    longtitude               = getLatLng(address)[1],
                                    category_id              = category.id,
                                    user_id                  = request.user,
                                )

            PlaceImage.objects.bulk_create(
                [PlaceImage(url = image['url'], place_id = place.id) for image in data['images']]
            )

            for tag in data['tags']:
                target_tag, flag = Tag.objects.get_or_create(name = tag['tag'])
                target_tag.places_tags.add(place)

            InvalidBookingDay.objects.bulk_create(
                [
                    InvalidBookingDay(
                        place_id = place.id,
                        day      = datetime.strptime(day['date'], '%Y-%m-%d')
                    ) for day in data['invalid_dates']
                ]
            )            
            
            return JsonResponse({"message":"SUCCESS"}, status = 201)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status = 400)
        
class UpdateDeletePlaceView(View):
    @transaction.atomic
    @check_auth_decorator
    def patch(self, request):
        try:
            data                           = json.loads(request.body)
            categories                     = Category.objects.filter(name = data['category'])
            
            if not categories:
                return JsonResponse({"message":"NOT_EXIST"}, status=400)
             
            category                       = categories.get()
            places                         = Place.objects.filter(id = data['id'], user_id = request_user)
            
            if not places:
                return JsonResponse({"message":"NOT_EXIST"}, status=400)

            place                          = places.get()            
            place.address                  = data['address']
            place.price_per_hour           = Decimal(data['price_per_hour'])
            place.area                     = data['area']
            place.floor                    = data['floor']
            place.region_id                = Region.objects.get(name = data['region']).id
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
            PlaceImage.objects.bulk_create(
                    [
                        PlaceImage( 
                            url = image['url'], place_id = place.id
                        ) for image in data['images']
                    ]             
                )

            for tag in data['tags']:
                target_tag, flag = Tag.objects.get_or_create(name = tag['tag'])
                target_tag.places.tags.add(place)
            
            InvalidBookingDay.objects.filter(place_id = place.id).delete()
            InvalidBookingDay.objects.bulk_create(
                    [
                        InvalidBookingDay(
                            place_id  = place.id,
                            day       = datetime.strptime(day['date'], '%Y-%m-%d')
                        ) for day in data['invalid_dates']
                    ]
                )

            return JsonResponse({"message":"SUCCESS"}, status = 201)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status = 400)

    @transaction.atomic
    @check_auth_decorator
    def delete(self, request):
        try:
            data     = json.loads(request.body)
            place_id = data["id"]
            
            Place.objects.filter(id = place_id, user_id = request.user).delete()

            return JsonResponse({"message":"SUCCESS"}, status = 204) 

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

def get_place_info(places):
    result = []
    slider_index = 0;
    
    try:
        for place in places:
            user = User.objects.get(id = place.user_id)

            result.append({
                'id'                    : slider_index,               # frontend측 slider 기능 사용위한 요청 데이터
                'place_id'              : place.id,
                'user_name'             : user.email,                 # 향후 nickname 데이터로 변경 필요(우선 email 반영)
                'avatar_img'            : user.thumbnail_url, 
                'category'              : place.category.name,
                'title'                 : place.title,
                'region'                : Region.objects.get(id = place.region_id).name,
                'price'                 : place.price_per_hour,
                'img_url'               : place.delegate_place_image_url,
                'floor'                 : place.floor,
                'area'                  : place.area,
                'maximun_parking_lot'   : place.minimum_rental_hour,
                'allowed_members_count' : place.allowed_members_count,
                'description'           : place.description,
                'using_rule'            : place.using_rule,
                'info_nearby'           : place.info_nearby,
                'minimum_rental_hour'   : place.minimum_rental_hour,
                'surcharge_rule'        : place.surcharge_rule,
                'latitude'              : place.latitude,
                'longtitude'            : place.longtitude, 
                'rating'                : [{
                                                "id"         : rate.id,
                                                "starpoint"  : rate.starpoint,
                                                "user_name"  : rate.user.name,
                                                "avatar_img" : rate.user.thumbnail_url,
                                                "created_at" : rate.created_at,
                                                "comments"   : rate.comment
                                            } for rate in Rating.objects.filter(place_id=place.id).order_by('-created_at')],
                'images_urls'           : [{"url":image.url} for image in PlaceImage.objects.filter(place_id = place.id)],
                'tags'                  : [{"tag":tag.name} for tag in Tag.objects.filter(places_tags__id = place.id)],
            })
            
            slider_index += 1

        return JsonResponse({'message':'SUCCESS','information':result}, status=200)   

    except KeyError:
        return JsonResponse({"message":"KEY_ERROR"}, status=400)

class PlaceView(View):
    @transaction.atomic
    @check_auth_decorator
    def post(self, request):
        try:
            data       = json.loads(reqeust.body)
            categories = Category.objects.filter(name = data['category'])

            if not categories:
                return JsonResponse({"message":"NOT_EXIST"}, status=400)

            address    = data['address']
            category   = categories.get()
            place      = Place.objects.create(
                                    address                  = address,
                                    price_per_hour           = Decimal(data['price_per_hour']),
                                    region_id                = Region.objects.get(name=data['region']).id,
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
                                    latitude                 = getLatLng(address)[0],
                                    longtitude               = getLatLng(address)[1],
                                    category_id              = category.id,
                                    user_id                  = request.user,
                                )

            PlaceImage.objects.bulk_create(
                [PlaceImage(url = image['url'], place_id = place.id) for image in data['images']]
            )

            for tag in data['tags']:
                target_tag, flag = Tag.objects.get_or_create(name = tag['tag'])
                target_tag.places_tags.add(place)

            InvalidBookingDay.objects.bulk_create(
                [
                    InvalidBookingDay(
                        place_id = place.id,
                        day      = datetime.strptime(day['date'], '%Y-%m-%d')
                    ) for day in data['invalid_dates']
                ]
            )            
            
            return JsonResponse({"message":"SUCCESS"}, status = 201)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status = 400)
      
    @check_auth_decorator
    def get(self, request):
        try:
            category_id = request.GET.get('category_id', None)
            search_text = request.GET.get('search_text', None)
            places      = None

            if category_id:
                category    = Category.objects.get(id = category_id)
                places      = Place.objects.filter(category_id = category_id)
            elif search_text:
                places = Place.objects.filter(
                            Q(title__contains = search_text) |
                            Q(description__contains = search_text) |
                            Q(region__name__contains = search_text) |
                            Q(category__name__contains = search_text)
                            )
            else:
                places = Place.objects.all()

            result = []
           
            if places:
                index = 0
                for place in places:
                    avg = 0.0
                    ratings = Rating.objects.filter(place_id=place.id)
                    if ratings:
                        avg = ratings.aggregate(Avg('starpoint'))
                        avg = round(avg['starpoint__avg'], 2)
                   
                    result.append({
                            'id'            : index,
                            'place_id'      : place.id,
                            'starpoint_avg' : avg,
                            'category'      : place.category.name,
                            'title'         : place.title,
                            'region'        : place.region.name,
                            'img_url'       : place.delegate_place_image_url,
                            'price_per_hour': place.price_per_hour,
                            'ratings'       : Rating.objects.filter(place_id=place.id).count(),
                        })
                    index += 1
            
            return JsonResponse({'message':'SUCCESS','information':result}, status=200)
        
        except Category.DoesNotExist:
            return JsonResponse({"message":"NOT_EXIST"}, status=404)

class GetDetailPlaceView(View):
    @check_auth_decorator
    def get(self, request, place_id):
        return get_place_info(Place.objects.filter(id = place_id))

class RemoveRatingView(View):
    @transaction.atomic
    @check_auth_decorator
    def delete(self, request, rating_id):
        try:
            Rating.objects.filter(id = rating_id).delete()

            return JsonResponse({"message":"SUCCESS"}, status=204)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

class RatingsView(View):
    @transaction.atomic
    @check_auth_decorator
    def post(self, request, place_id):
        try:
            data   = json.loads(request.body)
            rating = Rating.objects.create(
                            user_id   = request.user,
                            place_id  = place_id,
                            starpoint = data['starpoint'],
                            comment   = data['comment']
                        )
            result = {
                        'user_id'   : rating.user_id,
                        'place_id'  : rating.place_id,
                        'starpoint' : rating.starpoint,
                        'comment'   : rating.comment,
                    }
            return JsonResponse({"message":"SUCCESS", "information":result}, status=201)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

    @transaction.atomic
    @check_auth_decorator
    def get(self, request, place_id):
        try:
            offset = int(request.GET.get('offset', 0))
            limit  = int(request.GET.get('limit', 20))

            result = [
                 {
                        "id"         : rate.id,
                        "starpoint"  : rate.starpoint,
                        "user_name"  : rate.user.name,
                        "avatar_img" : rate.user.thumbnail_url,
                        "created_at" : rate.created_at,
                        "comment"    : rate.comment
                        } for rate in Rating.objects.select_related('user').filter(place_id = place_id)[offset:offset+limit]
            ]

            return JsonResponse({"message":"SUCCESS", "informations":result}, status=200)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)
'''
class SearchView(View):    
    @check_auth_decorator
    def get(self, request, search_text):
        search_info = []

        places = Place.objects.filter(
            Q(title__contains = search_text) |
            Q(description__contains = search_text) |
            Q(region__name__contains = search_text) |
            Q(category__name__contains = search_text)
            ).all()

        search_info = [
                {
                    'place_id'      : place.id,
                    'category'      : place.category.name,
                    'title'         : place.title,
                    'region'        : place.region.name,
                    'starpoint_avg' : Rating.objects.filter(place_id = place.id).aggregate(Avg('starpoint'))
                } for place in places]
            
        return JsonResponse({"message":"SUCCESS", "information":search_info},status=200)
'''
