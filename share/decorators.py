import json
import jwt

from django.http import JsonResponse

from user.models import (
                        User,
                    )
from my_settings import (
                        SECRET,
                        ALGORITHM,
                    )


def checkAuthDecorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            data      = json.loads(request.body)
            token     = request.headers['token']

            user_data = jwt.decode(
                                    token,
                                    SECRET['secret'],
                                    algorithm = ALGORITHM['hash'],
                                )

            if not User.objects.filter(id = user_data['user_id']).exists():
                return JsonResponse({"message":"INVALID_TOKEN"}, status=400)
                
            return func(self, request, *args, **kwargs)
            
        except json.JSONDecodeError:
            return JsonResponse({"message":"JSON_FORMAT_ERROR"}, status=400)

    return wrapper