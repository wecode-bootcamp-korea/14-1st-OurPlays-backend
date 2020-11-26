import json
import jwt
from datetime           import datetime
from decimal            import Decimal

from django.core            import serializers
from django.http            import JsonResponse, HttpResponse 
from django.views           import View 
from django.db.models       import Q, Avg
from django.db              import transaction

from share.kakaomap     import getLatLng
from share.decorators   import checkAuthDecorator
from .models            import *
from user.models        import *

class ReviewsView(View):
    # 평가 생성,보기 
    @checkAuthDecorator
    def post(self,request,place_id):
        user_id = request.headers['token']
        data = json.loads(request.body)
        try:
            user_info = User.objects.get(id=user_id)
            user = User.objects.filter(name=user_info.name,email=user_info.email)
            if user.exists():
                Rating.objects.create(
                    comment     = data['comment'],
                    place       = Place.objects.get(id=place_id),
                    user        = user_info,
                    starpoint   = data['starpoint']
                )
                return JsonResponse({'message':'SUCCESS'},status=200)
        
        except User.DoesNotExist:
            return JsonResponse({'message':'USER_DOSENOTEXIST'},status=401)
        
        except Place.DoesNotExist:
            return JsonResponse({'message':'PLACE_DOSENOTEXIST'},status=401)
    
    def get(self,request,place_id):
        try:
            # data = json.loads(request.body)
            ratings = Rating.objects.filter(place_id=place_id)
            reviews = []
            
            for rate in ratings:
                reviews.append({
                    "rate_id"  :rate.id, 
                    "starpoint":rate.starpoint,
                    "user_name":rate.user.name,
                    "created_at":rate.created_at,
                    "comments":rate.comment,
                })
            return JsonResponse({'message':'SUCCESS','place':reviews},status=200)
        
        except Place.DoesNotExist:
            return JsonResponse({'message':'PLACE_DOSENOTEXIST'},status=401)
  
class ReviewView(View):
    @checkAuthDecorator 
    def delete(self,request,rating_id):
        try:
            Rating.objects.filter(id=rating_id).delete()
            return JsonResponse({'message':f'id : {rating_id} 삭제'},status=200)
        
        except Rating.DoesNotExist:    
            return JsonResponse({'message':'RATING_DOSENOTEXIST'},status=401)
    @checkAuthDecorator 
    def put(self,request,rating_id):
        try:
            review_info = Rating.object.get(id=rating_id)
            review_info( 
                    starpoint = data['starpoint'],
                    comments = data['comment']
            ).save()
        except Exception as ex:
            return JsonResponse({'message':f'ex'},status=401)

class SearchView(View):
    # 검색기능
    def post(self,request):
        data = json.loads(request.body)
        search_info = []
        places = Place.objects.filter(
            Q(title__contains = data['search']) |
            Q(description__contains = data['search']) |
            Q(region__name__contains = data['search']) |
            Q(category__name__contains = data['search'])
            ).all()
        for place in places:
            ratings = place.related_rating_place.all()
            for rating in ratings:
                result=[]
                result.append(rating.starpoint)    
                sum_rating = sum(result)/ratings.count()
            
            search_info.append({
                'place_id'      : place.id,
                'category'      : place.category.name,
                'title'         : place.title,
                'region'        : place.region.name,
                'starpoint_avg' : sum_rating
                })
        
        return JsonResponse({'search':f'{search_info}'},status=200)

class PlaceDetailView(View):
    # Place 모든 정보
    def get(self,request,place_id):
        try:
            place = Place.objects.get(id=place_id)
            rating_values = []
            ratings = place.related_rating_place.all().order_by("-created_at")
            starpoint_count = ratings.count()
            result = []
            point_sum = 0 
            for rate in ratings:
                point_sum += rate.starpoint
                rating_values.append(
                    {
                        
                        "starpoint":rate.starpoint,
                        "user_name":rate.user.name,
                        "created_at":rate.created_at,
                        "comments":rate.comment,
                    })

            result.append({
                'category'              : place.category.name,
                'title'                 : place.title,
                'region'                : place.region.name,
                'img_url'               : place.delegate_place_image_url,
                'floor'                 : place.floor,
                'maximun_parking_lot'   : place.minimum_rental_hour,
                'allowed_members_count' : place.allowed_members_count,
                'description'           : place.description,
                'using_rule'            : place.using_rule,
                'info_nearby'           : place.info_nearby,
                'minimum_rental_hour'   : place.minimum_rental_hour,
                'surcharge_rule'        : place.surcharge_rule,
                'latitude'              : getLatLng(place.address)[0],
                'longitude'             : getLatLng(place.address)[1],
                'starpoint_avg'         : point_sum/starpoint_count,
                'rating'                : rating_values,
            })
            
            return JsonResponse({'message':'SUCCESS','place':result}, status=200)
        
        except Category.DoesNotExist:
            return JsonResponse({"message":"NOT_EXIST"}, status=404)

class PlacesView(View):
    def get(self,request,category_id):
        try:
            category = Category.objects.get(id=category_id)
            places = Place.objects.filter(category_id=category.id)
            result = []
            for place in places:
                ratings = Rating.objects.select_related('place').filter(place_id=place.id)
                rating_info = ratings.all().values('place_id').annotate(avg = Avg('starpoint'))
                result.append({
                        'rating_avg'    : rating_info.first()['avg'],  
                        'category'      : place.category.name,
                        'title'         : place.title,
                        'region'        : place.region.name,
                        'img_url'       : place.delegate_place_image_url,
                        'price_per_hour': place.price_per_hour,
                    })
            
            return JsonResponse({'message':'SUCCESS','place':result}, status=200)
        
        except Category.DoesNotExist:
            return JsonResponse({"message":"NOT_EXIST"}, status=404)

class CreatePlaceView(View):
    #@transaction.atomic
    @checkAuthDecorator
    def post(self, request):
        try:
            data       = json.loads(request.body)
            user_id    = request.user            
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
            
            PlaceImage.objects.bulk_create(
                [
                    PlaceImage( 
                        url      = image['url'],
                        place_id = place.id
                    ) for image in data['images']
                ]
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
    # @transaction.atomic
    @checkAuthDecorator
    def patch(self, request, place_id):
        try:
            data                           = json.loads(request.body)
            user_id                        = request.user
            categories                     = Category.objects.filter(name = data['category'])
            if not categories:
                return JsonResponse({"message":"NOT_EXIST"}, status=400)
             
            category                       = categories.get()
            places                         = Place.objects.filter(id = place_id, user_id = user_id)
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

    @checkAuthDecorator
    #@transaction.atomic
    def delete(self, quest, place_id):
        try:
            data     = json.loads(request.body)
            user_id  = request.user
            
            Place.objects.filter(id = place_id, user_id = user_id).delete()

            return JsonResponse({"message":"SUCCESS"}, status = 201) 

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)
