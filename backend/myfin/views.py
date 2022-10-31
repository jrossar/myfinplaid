
import ast
from itertools import product
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.country_code import CountryCode
from rest_framework import response
from urllib import request
from django.shortcuts import render
from rest_framework import viewsets
from .serializers import MyPlaidKeysSerializer, AuthenicateUserSerializer
from .models import MyFin
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie, csrf_protect
import json
from django.http import JsonResponse
from plaid.model.products import Products
from plaid.api import plaid_api
from datetime import datetime
from datetime import timedelta
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from .models import CustomAccountManager as cam
from .models import Transactions, NewUser
from rest_framework.views import APIView
from rest_framework.response import Response
import plaid
import time
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .UserHandler import UserHandler
import jwt
from myfin import serializers

# Create your views here.


def byte_to_str(a): return a.decode('UTF-8')


JWT_authenticator = JWTAuthentication()


logged_in_user = None


class MyTokenRefreshSerializer(TokenRefreshSerializer):
    @classmethod
    @csrf_exempt
    def refresh_token(self, response):
        print(response.method)
        print('YOLO BREH')
        return


class MyTokenRefreshView(TokenRefreshView):
    serializer_class = MyTokenRefreshSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    @csrf_exempt
    def get_token(self, user):
        token = super().get_token(user)
        print('!!!!!!!!!!GET TOKEN!!!!!!!!!!!!')
        # Add custom claims
        print(type(token))
        token['username'] = user.user_name
        token['userId'] = user.id
        print(user)
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@ensure_csrf_cookie
def csrf(request):
    response = JsonResponse({'csrfToken': get_token(request)})
    response['Access-Control-Allow-Origin'] = 'http://localhost:3000/'
    return response


def ping(request):
    print(request.method)
    if (request.method == 'POST'):
        print('hello')
        return JsonResponse({'result': 'OK'})
    if (request.method == 'OPTIONS'):
        print('hello')


@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    def get(self, request, format=None):
        return Response({'success': 'CSRF cookie set'})


class MyFinView(viewsets.ModelViewSet):
    serializer_class = MyPlaidKeysSerializer
    # queryset = MyFin.objects.all()


class PlaidApiInfo(viewsets.ViewSet):
    item_id = None
    access_token = None
    products = ['transactions']


data = {}

PLAID_ENV = 'sandbox'

if PLAID_ENV == 'sandbox':
    host = plaid.Environment.Sandbox
elif PLAID_ENV == 'development':
    host = plaid.Environment.Development


PLAID_CLIENT_ID = '61647a5be37dd70012bcd2bc'
PLAID_SECRET = '821b48026f3e63f97fad1432e4e8a4'
print(PLAID_CLIENT_ID, PLAID_SECRET)

configuration = plaid.Configuration(
    host=host,
    api_key={
        'clientId': PLAID_CLIENT_ID,
        'secret': PLAID_SECRET,
        'plaidVersion': '2020-09-14'
    }
)
api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)


@csrf_exempt
def create_link_token(request):
    print(request.method)
    if request.method == 'POST':
        data = byte_to_str(request.body)
        print('DATA: ' + data)
        data = json.loads(data)
        PLAID_COUNTRY_CODES = ['US']
        products = [Products('transactions')]
        plaid_request = LinkTokenCreateRequest(
            products=products,
            client_name="Plaid Quickstart",
            country_codes=list(
                map(lambda x: CountryCode(x), PLAID_COUNTRY_CODES)
            ),
            language='en',
            user=LinkTokenCreateRequestUser(
                client_user_id=str(time.time())
            )
        )

        # create link token
        response = client.link_token_create(plaid_request)
        print(response.to_dict())
        return JsonResponse(response.to_dict())


@ csrf_exempt
def authenticate_user(request):
    data = {'status': 'fail'}
    if request.method == 'POST':
        mttops = MyTokenObtainPairSerializer()
        data = byte_to_str(request.body)
        data = json.loads(data)
        print('~~~~~~~~~~~~SESSIONKEY~AuthenticateUser~~~~~~~~~~~~~')
        print(request.session.session_key)
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print(data)
        print(type(data))
        email = data['username']
        password = data['password']
        user = authenticate(request, username=email, password=password)
        print(user.is_authenticated)
        if user is not None:
            print('session keys:', request.session.keys())
            login(request, user)
            data = {
                'status': 'success',
                'user': user.user_name,
                'user_id': user.id,
                'session_key': request.session.session_key,
            }
            data['token'] = mttops.get_token(user)

            print('setting session username')
            print(request.session.session_key)
            # print(Session.objects[0])
            print(request.session.get('user'))
            print(user.id)
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~JWT TOKEN~~~~~~~~~~~~~~~~~~')
            print(data['token'])
            print(type(data['token']))
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~END~~~~~~~~~~~~~~~~~~')
        else:
            data = {'status': 'fail'}
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~JSON Response~~~~~~~~~~~~~~~~~~')
        ret = JsonResponse({'data': {'hello': '1'}})
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~Print Readable~~~~~~~~~~~~~~~~~~')
        print(ret.readable())
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~Print Content~~~~~~~~~~~~~~~~~~')
        print(ret.content)
        return ret
    if request.method == 'OPTIONS':
        print('hi')
    return JsonResponse({'data': data})


def get_user_data(jwt_token):
    user_data = jwt.decode(
        jwt_token,
        'B13S413OIPOASD1231)&%$&*HHFLKAHSDJK791723012UOF)&%$&*',
        algorithms='HS256'
    )
    user = NewUser.objects.get(id=user_data['userId'])
    return user


def get_data(byte_data):
    data = byte_data(request.body)
    return json.loads(data)


@csrf_exempt
def user_info(request):
    if request.method == 'POST':
        print('~~~~~~~~~inside user info~~~~~~~~~')
        data = byte_to_str(request.body)
        data = json.loads(data)
        # include user_id / username in authenticate user function
        print(data['sessionKey'])
        s = Session.objects.get(pk=data['sessionKey'])
        print(s.get_decoded())
        return JsonResponse({'status': 'success'})

    if request.method == 'GET':
        print(request.session.keys())
        print(request.session.items())
        print(request.session.get('user'))
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'success'})


@csrf_exempt
class AuthenticateUserView(APIView):
    serializer_class = AuthenicateUserSerializer

    def post(self, request, format=None):
        print(request.data)
