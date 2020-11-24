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


def check_auth_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            data         = json.loads(request.body)
            token        = request.headers['token']
            user_data    = jwt.decode(
                                    token,
                                    SECRET['secret'],
                                    algorithm = ALGORITHM['hash'],
                                    )
            request.user = user_data["user_id"]
                
            return func(self, request, *args, **kwargs)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)
        except jwt.exceptions.InvalidTokenError:
            return JsonResponse({"message":"INVALID_TOKEN"}, status=400)


    return wrapper

