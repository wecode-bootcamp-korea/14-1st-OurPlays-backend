import json
import jwt

from django.http import JsonResponse

from user.models import User

from my_settings import SECRET_KEY, ALGORITHM
                
def checkAuthDecorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            data    = json.loads(request.body)
            token   = request.headers['token']
            user_data   = jwt.decode(
                                token, 
                                SECRET_KEY['secret'], 
                                algorithm = ALGORITHM['hash'],
                                )
    
            if not User.objects.filter(id=user_data['user_id']).exists():
                raise Exception()

                
            return func(self, request, *args, **kwargs)
            
        except json.JSONDecodeError:
            return JsonResponse({"message":"JSON_FORMAT_ERROR"}, status=400)
        except Exception:
            return JsonResponse({"message":"INVALIABLE_REQUEST"}, status=400)

    return wrapper
