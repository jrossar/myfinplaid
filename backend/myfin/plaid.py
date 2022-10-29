from os import access
from django.views.decorators.csrf import csrf_exempt
import time
import plaid
from datetime import timedelta
from datetime import datetime
from plaid.api import plaid_api
import json
from plaid.model.ach_class import ACHClass
from plaid.model.transfer_user_address_in_request import TransferUserAddressInRequest
from plaid.model.transfer_user_in_request import TransferUserInRequest
from plaid.model.transfer_create_idempotency_key import TransferCreateIdempotencyKey
from plaid.model.transfer_type import TransferType
from plaid.model.transfer_create_request import TransferCreateRequest
from plaid.model.transfer_network import TransferNetwork
from plaid.model.transfer_authorization_create_request import TransferAuthorizationCreateRequest
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.country_code import CountryCode
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.products import Products
from django.http import JsonResponse
from .handle_models import save_transactions
from rest_framework_simplejwt.authentication import JWTAuthentication
from .views import JWT_authenticator, byte_to_str, get_user_data
from .models import NewUser
import jwt


class Plaid:
    JWT_authenticator = JWTAuthentication()
    PLAID_CLIENT_ID = '61647a5be37dd70012bcd2bc'
    PLAID_SECRET = '821b48026f3e63f97fad1432e4e8a4'
    # PLAID_SECRET = 'b5eab137a1b201458e2cbdccfcd13f'
    PLAID_PRODUCTS = ['transactions']
    # PLAID_ENV = 'development'
    PLAID_ENV = 'sandbox'

    if PLAID_ENV == 'sandbox':
        host = plaid.Environment.Sandbox
    elif PLAID_ENV == 'development':
        host = plaid.Environment.Development
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

    access_token = None

    def authorize_and_create_transfer(self, access_token):
        try:
            # We call /accounts/get to obtain first account_id - in production,
            # account_id's should be persisted in a data store and retrieved
            # from there.
            request = AccountsGetRequest(access_token=access_token)
            response = self.client.accounts_get(request)
            account_id = response['accounts'][0]['account_id']

            request = TransferAuthorizationCreateRequest(
                access_token=access_token,
                account_id=account_id,
                type=TransferType('credit'),
                network=TransferNetwork('ach'),
                amount='1.34',
                ach_class=ACHClass('ppd'),
                user=TransferUserInRequest(
                    legal_name='FirstName LastName',
                    email_address='foobar@email.com',
                    address=TransferUserAddressInRequest(
                        street='123 Main St.',
                        city='San Francisco',
                        region='CA',
                        postal_code='94053',
                        country='US'
                    ),
                ),
            )
            response = self.client.transfer_authorization_create(request)
            self.pretty_print_response(response)
            authorization_id = response['authorization']['id']

            request = TransferCreateRequest(
                idempotency_key=TransferCreateIdempotencyKey(
                    '1223abc456xyz7890001'),
                access_token=access_token,
                account_id=account_id,
                authorization_id=authorization_id,
                type=TransferType('credit'),
                network=TransferNetwork('ach'),
                amount='1.34',
                description='Payment',
                ach_class=ACHClass('ppd'),
                user=TransferUserInRequest(
                    legal_name='FirstName LastName',
                    email_address='foobar@email.com',
                    address=TransferUserAddressInRequest(
                        street='123 Main St.',
                        city='San Francisco',
                        region='CA',
                        postal_code='94053',
                        country='US'
                    ),
                ),
            )
            response = self.client.transfer_create(request)
            self.pretty_print_response(response)
            return response['transfer']['id']
        except plaid.ApiException as e:
            error_response = self.format_error(e)
            return JsonResponse(error_response)

    @csrf_exempt
    def create_link_token(self, request):
        print(request.method)
        print(request.session.session_key)
        phone_number_data = byte_to_str(request.body)
        phone_number = json.loads(phone_number_data)
        print('phone number data', phone_number_data)
        print('~~~~~~~~~~~~SESSIONKEY~CreateLinkToken~~~~~~~~~~~~~')
        print(request.session.session_key)
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
                client_user_id=str(time.time()),
                phone_number=phone_number['phone_number'])
        )

        # create link token
        response = self.client.link_token_create(plaid_request)
        print(response.to_dict())
        if request.method == 'POST':
            return JsonResponse(response.to_dict())

    def format_error(e):
        response = json.loads(e.body)
        return {'error': {'status_code': e.status, 'display_message':
                          response['error_message'], 'error_code': response['error_code'], 'error_type': response['error_type']}}

    @csrf_exempt
    def get_access_token(self, request):
        global access_token
        global item_id
        global transfer_id
        if request.method == 'POST':
            print('~~~~~~~~~~~~INSIDE GET ACCESS TOKEN~~~~~~~~~~~~~~~~~~~~')
            print(request.body)
            data = byte_to_str(request.body)
            print('Setting Data')
            data = json.loads(data)
            print('Setting public token')
            public_token = data['public_token']
            print('public_token', public_token)
            jwt_token = data['JWT_Token']
            print('JWT_Token', jwt_token)

            try:
                exchange_request = ItemPublicTokenExchangeRequest(
                    public_token=public_token)
                exchange_response = self.client.item_public_token_exchange(
                    exchange_request)
                access_token = exchange_response['access_token']
                item_id = exchange_response['item_id']
                user = get_user_data(jwt_token)
                user.access_token = access_token
                user.save()
                print(user.access_token)
                if 'transfer' in self.PLAID_PRODUCTS:
                    transfer_id = self.authorize_and_create_transfer(
                        access_token)
                return JsonResponse(exchange_response.to_dict())
            except plaid.ApiException as e:
                return json.loads(e.body)

    @ csrf_exempt
    def get_info(self, request):
        data = {
            'item_id': None,
            'access_token': None,
            'products': self.PLAID_PRODUCTS
        }
        if request.method == 'POST':
            return JsonResponse({
                'item_id': None,
                'access_token': None,
                'products': self.PLAID_PRODUCTS
            })

    @ csrf_exempt
    def get_keys(request):
        KEYS = {
            'client_id': '61647a5be37dd70012bcd2bc',
            'secret_id': '821b48026f3e63f97fad1432e4e8a4'
        }
        if request.method == 'POST':
            return JsonResponse(KEYS)
        if request.method == 'GET':
            return JsonResponse(KEYS)

    @ csrf_exempt
    def get_transactions(self, request):
        # Pull transactions for the last 30 days
        start_date = (datetime.now() - timedelta(days=30))
        end_date = datetime.now()
        print('Get Transactions request.method')
        print(request.method)
        if request.method == 'POST':
            print('INSIDE GET TRANSACTIONS')
            data = byte_to_str(request.body)
            data = json.loads(data)
            print(data)
            print(data['JWT_Token'])
            user = get_user_data(data['JWT_Token'])
            try:
                options = TransactionsGetRequestOptions()
                plaid_request = TransactionsGetRequest(
                    access_token=user.access_token,
                    start_date=start_date.date(),
                    end_date=end_date.date(),
                    options=options
                )
                response = self.client.transactions_get(plaid_request)
                # self.pretty_print_response(response.to_dict())
                self.handle_transactions(response.to_dict())
                return JsonResponse(response.to_dict())
            except plaid.ApiException as e:
                error_response = self.format_error(e)
                return JsonResponse(error_response)
        return JsonResponse(request)

    def handle_transactions(self, transactions):
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print(len(transactions['accounts']))
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print(len(transactions['transactions']))
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print(transactions['total_transactions'])
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print(transactions['item'])
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print(transactions['request_id'])
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print(transactions['transactions'][0])
        for transaction in transactions['transactions']:
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            print(transaction)

    def pretty_print_response(self, response):
        print(json.dumps(response, indent=2, sort_keys=True, default=str))
