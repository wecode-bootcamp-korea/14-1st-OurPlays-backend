import json
import jwt

from django.db.models import Q
from django.core import serializers
from django.http import JsonResponse
from django.views import View

from .models import (
                Place,
        )
from share.decorators import checkAuthDecorator


class AddPlaceView(View):
    @checkAuthDecorator
    def post(self, request):
        data = json.loads(request.body)
         
        
        '''
        1. address
        2. price_per_hour
        3. area
        4. floor
        5. maximum_parking_lot
        6. allowed_members_count
        7. description
        8. using_rule
        9. info_nearby
        10. minimum_rental_hour
        11. delegate_place_image_url(실제론 이미지 파일이 날라오므로 이미지를 저장해야 함)
        12. surcharge_rule (할증 옵션값)
        13. category_id
        14. user_id
        '''

