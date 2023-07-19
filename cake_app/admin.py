from django.contrib import admin
from .models import Client, Order, ReadyCake


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ["client_tg_id", "client_tg_username"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["address", "delivery_date", "delivery_time", "is_active"]


@admin.register(ReadyCake)
class ReadyCake(admin.ModelAdmin):
    list_display = ["cake_name", "cake_price"]
