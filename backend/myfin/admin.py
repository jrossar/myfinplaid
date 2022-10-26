from django.contrib import admin
from .models import MyFin
from .models import Transactions

admin.register(Transactions)


class MyFinAdmin(admin.ModelAdmin):
  key_display = ('secret_key', 'client_id')

# Register your models here.
admin.site.register(MyFin, MyFinAdmin)