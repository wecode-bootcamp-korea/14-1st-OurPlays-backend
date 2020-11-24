import re
import jwt
import json
import bcrypt

from django.db        import models
from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q
from my_settings      import SECRET_KEY, ALGORITHM

from .models          import User

class SignUp(View):
    def post(self, request):
        data           = json.loads(request.body)
        check_email    = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        check_password = re.compile('^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$')
        #최소 8자, 최소 하나의 문자, 하나의 숫자 및 하나의 특수 문자
        
        if not 'email' in data:
            return JsonResponse({'message':'EMAIL_ERROR'}, status=400)
            
        if not re.match(check_email, data['email']):
            return JsonResponse({'message':'BAD_EMAIL_REQUEST'}, status=400)
            
        if not re.match(check_password, data['password']):
            return JsonResponse({'message':'PASSWORD1_ERROR'}, status=400)
        
        if not re.match(check_password, data['repassword']):
                return JsonResponse({'message':'PASSWORD_ERROR'}, status=400)

        if data['password'] != data['repassword']:
                return JsonResponse({'message':'PASSWORD_INCONSISTENCY'}, status=400)
                            
        if User.objects.filter(email = data['email']).exists():
             return JsonResponse({'message':'EXISTS_USER'}, status=400)
        
        user = User.objects.create(
            email    = data['email'],
            password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode(),
        )
        return JsonResponse({'message':'SUCCESS_SIGNUP'}, status=200)
        
       
class SignIn(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if 'email' not in data or 'password' not in data:
                return JsonResponse({'message':'CHECK_DATA'}, status=400)

            if not User.objects.filter(emai l= data['email']).exists():
                return JsonResponse({'message':'INVALITD_USER'}, status=400)

            user_data = User.objects.get(email = data['email'])

            if bcrypt.checkpw(data['password'].encode('utf-8'), user_data.password.encode('utf-8')):
                token = jwt.encode({'email':user_data.email}, SECRET_KEY['secret'], algorithm = ALGORITHM['hash']).decode('utf-8')
                return JsonResponse({'message':'SUCCESS_LOGIN', 'token':token}, status=200)

            return JsonResponse({'message':'INVALID_PASSWORD'}, status=400)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=401)