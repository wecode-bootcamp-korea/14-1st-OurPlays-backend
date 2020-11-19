import json

from django.http    import JsonResponse, HttpResponse
from django.views   import View 

from share.decorators   import checkAuthDecorator
from .models            import *


class PlaceView(View):
    def get(self,request):
        data = json.loads(request.body)
        category = Category.objects.get(name=data["category"])
        
        places = Place.objects.filter(category_id=category.id)
        result = []
        
        for place in places:
            rating_values = []
            ratings = Rating.objects.filter(place_id = place.id).order_by("-created_at")

            for rate in ratings:
                rating_values.append(
                    {
                        "starpoint":rate.starpoint,
                        "user_name":rate.user.name,
                        "created_at":rate.created_at,
                        "comments":rate.comment,
                    })

            # grades_list = list(place.related_rating_place.all())
            result.append({
                'category'              : place.category.name,
                'title'                 : place.title,
                'region'                : place.region,
                'price'                 : place.price_per_hour,
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
        

        




# class SlideView(View):


# class BestShootingPlace(View):


# class CategoryView(View):
