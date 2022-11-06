from .models import CustomAccountManager
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from myfin import views
import json


class UserHandler():
    account_manager = CustomAccountManager()

    @csrf_exempt
    def create_user(self, request):
        if request.method == 'POST':
            print(request.body)
            data = views.byte_to_str(request.body)
            data = json.loads(data)
            print(data)
            self.account_manager.create_user(
                email=data['email'],
                user_name=data['userName'],
                password=data['password'],
                phone_number=data['phoneNumber']
            )
            return JsonResponse({'response': 'sucess'})

        account_manager.create_user(
            email=user['email'],
            user_name=user['userName'],
            password=user['password'],
            phone_number=user['phoneNumber'],
        )
        return JsonResponse({'hello': 'banana'})
