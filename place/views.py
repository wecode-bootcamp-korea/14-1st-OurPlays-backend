import json

from django.http        import JsonResponse, HttpResponse 
from django.views       import View 
from django.db.models   import Q, Count, Avg

from share.decorators   import checkAuthDecorator
from .models            import *
from user.models        import *
# class Test(View):
#     def get(self, request):
#         # @checkAuthDecorator
#         data = json.loads(request.body)
#         try:
#             places = Place.objects.prefetch_related('related_rating_place').all()
#             result=[]
#             place_rating = []
#             place_id = []
#             dict_place = {}
#             for place in places:
#                 ratings = place.related_rating_place.all()
#                 for rating in ratings:
#                     result=[]
#                     result.append(rating.starpoint)    
#                 sum_rating = sum(result)/ratings.count()
#                 place_rating.append(sum_rating)
#                 dict_place[sum_rating] = place.id
#             print(dict_place)
#             return JsonResponse({'message':f'{dict_place}'},status=200)
        
#         except Exception as ex:
#             return JsonResponse({'message':'bye'},status=200)

class ReviewsView(View):
    # 평가 생성,보기 
    # @checkAuthDecorator
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
    def delete(self,request,rating_id):
        try:
            Rating.objects.filter(id=rating_id).delete()
            return JsonResponse({'message':f'id : {rating_id} 삭제'},status=200)
        
        except Rating.DoesNotExist:    
            return JsonResponse({'message':'RATING_DOSENOTEXIST'},status=401)
    
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



class PlaceView(View):
    # Place 모든 정보
    def get(self,request,category_id):
        #data = json.loads(request.body)
        category = Category.objects.get(id=category_id)
        places = Place.objects.filter(category_id=category.id)
        result = []
        
        for place in places:
            rating_values = []
            ratings = place.related_rating_place.all().order_by("-created_at")

            for rate in ratings:
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
                'rating'                : rating_values,
            })
            
        return JsonResponse({'message':'SUCCESS','place':result}, status=200)

class PlacesView(View):
    def get(self,request,category_id):
        category = Category.objects.get(id=category_id)
        places = Place.objects.filter(category_id=category.id)
        result = []
        
        for place in places:
            ratings = Rating.objects.select_related('place').filter(place_id=place.id)
            rating_info = ratings.all().values('place_id').annotate(avg = Avg('starpoint'))
            result.append({
                    'rating_avg' : rating_info.first()['avg'],  
                    'category'   : place.category.name,
                    'title'      : place.title,
                    'region'     : place.region.name,
                    'img_url'    : place.delegate_place_image_url,
                })
        
        return JsonResponse({'message':'SUCCESS','place':result}, status=200)

    