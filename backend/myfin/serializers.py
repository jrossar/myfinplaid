from rest_framework import serializers
from .models import MyFin, NewUser


class MyPlaidKeysSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyFin
        fields = ('id', 'secret_key', 'client_id')


class MyPlaidInfoSerializer(serializers.Serializer):
    def __init__(self, item_id, access_token, products):
        self.item_id = item_id
        self.access_token = access_token
        self.products = products

class AuthenicateUserSerializer(serializers.Serializer):
    class Meta:
        model = NewUser
        fields = ('email', 'password')

serializer = MyPlaidInfoSerializer(None, None, ['transactions'])
