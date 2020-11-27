import re
import jwt
import json
import bcrypt

from django.db import models
from django.http import JsonResponse
from django.views import View
from django.db.models import (
                                Q,
                                Count
                            )
from my_settings import SECRET, ALGORITHM

from .models import (
                    User,
                    PlaceMark,
                    )
from place.models import (
                            Place,
                            Rating
                        )
from share.decorators import check_auth_decorator

class SignUpView(View):
    def post(self, request):
        try:
            
            data           = json.loads(request.body)
            check_email    = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
            check_password = re.compile('^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$')

            if not 'email' in data:
                return JsonResponse({'message':'EMAIL_ERROR'}, status=400)
                
            if not re.match(check_email, data['email']):
                return JsonResponse({'message':'BAD_EMAIL_REQUEST'}, status=400)
                
            if User.objects.filter(email = data['email']).exists():
                 return JsonResponse({'message':'EXISTS_USER'}, status=400)
            
            if not re.match(check_password, data['password']):
                return JsonResponse({'message':'INVALID_PASSWORD'}, status=400)
            
            #if not re.match(check_password, data['password2']):
            #    return JsonResponse({'message':'PASSWORD1_ERROR'}, status=400)

            #if data['password'] != data['password2']:
            #    return JsonResponse({'message':'PASSWORD_INCONSISTENCY'}, status=400)
            
            user = User.objects.create(
                name          = data['name'],
                email         = data['email'],
                password      = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode(),
                thumbnail_url = '',
            )

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

        return JsonResponse({'message':'SUCCESS'}, status=201)
       
class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if not 'email' in data or not 'password' in data:
                return JsonResponse({'message':'CHECK_DATA'}, status=400)

            users = User.objects.filter(email=data['email'])
            if not users.exists():
                return JsonResponse({'message':'INVALITD_USER'}, status=400)

            #user_data = User.objects.get(email=data['email'])
            user_data = users.get()

            if bcrypt.checkpw(data['password'].encode('utf-8'), user_data.password.encode('utf-8')):
                token = jwt.encode({'user_id':user_data.id}, SECRET['secret'], algorithm = ALGORITHM['hash']).decode('utf-8')
                return JsonResponse({'message':'SUCCESS_LOGIN', 'token':token}, status=200)

            return JsonResponse({'message':'INVALID_PASSWORD'}, status=400)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=401)

class MarkingPlaceView(View):
    @check_auth_decorator
    def post(self, request):
        try:
            data        = json.loads(request.body)
            place_id    = data["place_id"]
            place_marks = PlaceMark.objects.filter(place_id = place_id, user_id = request.user)
            
            if place_marks:
                place_marks.delete()
            else:
                PlaceMark.objects.create(place_id = place_id, user_id = request.user)

            return JsonResponse({"message":"SUCCESS"}, status = 201)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

class GetMarkedPlacesView(View):
    @check_auth_decorator
    def get(self, request):
        try:            
            offset = int(request.GET.get('offset', 0))
            limit  = int(request.GET.get('limit', 20))

            result = [
                {
                    'id'        : place_mark.place.id,
                    'title'     : place_mark.place.title,
                    'img_url'   : place_mark.place.delegate_place_image_url,
                    'category'  : place_mark.place.category.name,
                    'region'    : place_mark.place.region.name,
                    'price'     : place_mark.place.price_per_hour,
                    'ratings'   : [{
                                        "id"         : rate.id,
                                        "starpoint"  : rate.starpoint,
                                        "user_name"  : rate.user.name,
                                        "avatar_img" : rate.user.thumbnail_url,
                                        "created_at" : rate.created_at,
                                        "comments"   : rate.comment
                                    } for rate in Rating.objects.filter(place_id = place_mark.place.id)
                                        .order_by('-created_at')]
                    } for place_mark in PlaceMark.objects.select_related('place').filter(user_id = request.user)[offset:offset+limit]
            ]

            return JsonResponse({"message":"SUCCESS", "information":result}, status = 201)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)



