import imp
from pyexpat import model
from unicodedata import category, decimal, name
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.forms import CharField
from django.utils import timezone, timesince

# Create your models here.


class CustomAccountManager(BaseUserManager):
    def create_user(self, email, user_name, password, phone_number, **other_fields):
        print('Email')
        email = self.normalize_email(email)
        print('Creating User!')
        user = NewUser(email=email, user_name=user_name,
                       phone_number=phone_number)
        print('Setting Password!')
        user.set_password(password)
        print('saving!!')
        user.save()
        print('returning!!')
        return user

    def create_superuser(self, email, user_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be staff')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True')

        return self.create_user(email, user_name, password, **other_fields)


class MyFin(models.Model):
    secret_key = models.CharField(max_length=24)
    client_id = models.CharField(max_length=24)

    def __str__(self):
        return 'Secret Plaid Keys'


class NewUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('Email', max_length=320, unique=True)
    user_name = models.CharField('User Name', max_length=150, unique=True)
    first_name = models.CharField('First Name', max_length=20)
    password = models.CharField('Password', max_length=30)
    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField('Is Staff', default=False)
    is_superuser = models.BooleanField('Is Superuser', default=False)
    id = models.AutoField(primary_key=True)
    is_active = models.BooleanField('Is Active', default=True)
    access_token = models.CharField(
        'Access_Token', max_length=60, default='no_access_token'
    )
    phone_number = models.CharField(
        'Phone Number', max_length=12, default='not_provided')
    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'phone_number']

    def __str__(self):
        return self.user_name


class Transactions(models.Model):
    transaction_id = models.CharField('Transaction ID', max_length=42)
    category = models.CharField('Transaction ID', max_length=30)
    name = models.CharField('Name', max_length=40)
    amount = models.DecimalField('Amount', max_digits=8, decimal_places=2)
    pending = models.BooleanField('Pending')
    iso_currency_code = models.CharField("Currency", max_length=10)
    account_id = models.CharField('Account ID', max_length=40)
    date = models.DateTimeField('Date of Transaction', default=timezone.now)
    # Look up SQL for more on_delete actions
    user_id = models.ForeignKey(NewUser, on_delete=models.CASCADE)

    def __str__(self):
        describe_transaction = f'Trans ID: {self.transaction_id}, Name: {self.name}, Amount: {self.amount}'
        return describe_transaction


print(NewUser.objects.all())
